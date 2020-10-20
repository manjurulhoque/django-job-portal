from django.apps import apps

from jobs.celery import app as celery_app

from .events import EVENTS
from .providers import PROVIDERS
from .settings import ASYNC_QUEUE_NAME, PROVIDERS_SETTINGS


@celery_app.task(queue=ASYNC_QUEUE_NAME)
def dispatch_event(event_name: str, model_label: str, instance_pk: int):
    """
    Called from event_decorator. Get provider codes from event name, iterate each one and if provider
    is enabled, dispatch a new async task for processing.
    """
    provider_codes = EVENTS[event_name]
    for provider_code in provider_codes:
        if PROVIDERS_SETTINGS[provider_code]["enabled"]:
            dispatch_event_provider.delay(provider_code, event_name, model_label, instance_pk)


@celery_app.task(bind=True, queue=ASYNC_QUEUE_NAME)
def dispatch_event_provider(
    self, provider_code: str, event_name: str, model_label: str, instance_pk: int
):
    """
    It processes a provider publish. It something goes wrong, it's retried "n" times.
    """

    # Getting the model and instance
    model = apps.get_model(model_label)
    try:
        model_instance = model.objects.get(pk=instance_pk)
    except model.DoesNotExist:
        return

    # Instantiating provider class and publishing
    provider = PROVIDERS[provider_code]()
    success = provider.publish(event_name, model_instance)
    if not success:
        self.retry(max_retries=PROVIDERS_SETTINGS[provider_code]["max_retries"], countdown=30)
