import json
import os
from logging import getLogger

from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.trace import INVALID_SPAN, SpanKind
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.propagate import extract
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry import context, trace

from helios.instrumentation import HeliosBaseInstrumentor

_LOG = getLogger(__name__)

MODULE_NAME = 'opentelemetry.instrumentation.aws_lambda'


def _custom_event_context_extractor(event):
    ctx = None
    if 'detail-type' in event:
        # Eventbridge case
        if 'detail' in event and 'headers' in event['detail']:
            headers = event['detail']['headers']
        if headers is None and 'headers' in event:
            headers = event['headers']
        if headers is not None:
            ctx = extract(headers)

    if 'headers' in event:
        ctx = extract(event['headers'])

    if ctx is not None and trace.get_current_span(ctx) != INVALID_SPAN:
        return ctx

    return context.Context()


def wrap_lambda_function(original_handler, tracer_provider):
    lambda_handler = os.environ.get('ORIG_HANDLER', os.environ.get('_HANDLER'))
    wrapped_module_name, wrapped_function_name = lambda_handler.rsplit('.', 1)

    def wrapped_lambda(*args, **kwargs):
        orig_handler_name = '.'.join([wrapped_module_name, wrapped_function_name])
        lambda_event = args[0]
        parent_context = _custom_event_context_extractor(lambda_event)

        try:
            if lambda_event['Records'][0]['eventSource'] in {
                'aws:sqs',
                'aws:s3',
                'aws:sns',
                'aws:dynamodb',
            }:
                span_kind = SpanKind.CONSUMER
            else:
                span_kind = SpanKind.SERVER
        except (IndexError, KeyError, TypeError):
            span_kind = SpanKind.SERVER

        tracer = tracer_provider.get_tracer(MODULE_NAME)

        with tracer.start_as_current_span(
                name=orig_handler_name,
                context=parent_context,
                kind=span_kind,
        ) as span:
            if span.is_recording():
                lambda_context = args[1]
                span.set_attribute(
                    ResourceAttributes.FAAS_ID,
                    lambda_context.invoked_function_arn,
                )
                span.set_attribute(
                    SpanAttributes.FAAS_EXECUTION,
                    lambda_context.aws_request_id,
                )
                HeliosBaseInstrumentor.set_payload_attribute(span, 'faas.event', json.dumps(lambda_event))

            result = None
            try:
                result = original_handler(*args, **kwargs)
            except Exception as err:
                span.set_status(Status(status_code=StatusCode.ERROR, description=str(err)))
                raise err
            HeliosBaseInstrumentor.set_payload_attribute(span, 'faas.res', json.dumps(result))

        if hasattr(tracer_provider, 'force_flush'):
            try:
                tracer_provider.force_flush(30000)
            except Exception:  # pylint: disable=broad-except
                _LOG.exception("TracerProvider failed to flush traces")

        return result

    return wrapped_lambda
