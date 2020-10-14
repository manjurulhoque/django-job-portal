from . import *  # noqa

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "project": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "": {"handlers": ["console"], "level": "INFO", "propagate": True},
    },
}
