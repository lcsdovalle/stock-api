"""
Staging settings.
"""
from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = env.list("STAGING_ALLOWED_HOSTS", default=[])  # noqa


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "rotating_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/dev.log",  # noqa
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 7,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["rotating_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["rotating_file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
