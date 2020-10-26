from django.conf import settings

# Getting project settings
PROJECT_PROVIDER_SETTINGS = getattr(settings, "NOTIFICATIONS", {})

# Internal module settings be merged with project settings
PROVIDERS_SETTINGS = {
    **{
        "telegram": {
            "enabled": False,
            "max_retries": 5,
        },
        "twitter": {
            "enabled": False,
            "max_retries": 5,
        },
    },
    **PROJECT_PROVIDER_SETTINGS,
}

NOTIFICATIONS_ENABLED = any([provider["enabled"] for provider in PROVIDERS_SETTINGS.values()])

ASYNC_QUEUE_NAME = getattr(settings, "NOTIFICATIONS_ASYNC_QUEUE_NAME", "default")
