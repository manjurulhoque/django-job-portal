from .settings import NOTIFICATIONS_ENABLED
from .tasks import dispatch_event


def event_dispatcher(event_name: str):
    """
    Decorator for models to dispatch an event on save a new record.
    Example:

        from notifications.decorators import event_dispatcher
        from notifications.events import EVENT_NEW_JOB

        @event_dispatcher(EVENT_NEW_JOB)
        class Job(models.Model):
            pass
    """

    def decorator(cls):
        def save(self, *args, **kwargs):
            is_new = not self.pk
            save._original(self, *args, **kwargs)
            # Only if it's a new record and all notification's providers are enabled.
            if is_new and NOTIFICATIONS_ENABLED:
                dispatch_event.delay(event_name, self._meta.label, self.pk)

        save._original = cls.save
        cls.save = save
        return cls

    return decorator
