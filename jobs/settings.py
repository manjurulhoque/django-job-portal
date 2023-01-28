import os
import sys
from datetime import timedelta

import environ
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

env = environ.Env()

SECRET_KEY = "@pzqp#x^+#(olu#wy(6=mi9&a8n+g&x#af#apn07@j=5oin=xb"

DEBUG = env("DEBUG", default=False)
print("DEBUG: ", DEBUG)

# DEBUG = True
SITE_ID = 1
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django_elasticsearch_dsl",
    "drf_yasg",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "jobsapp",
    "resume_cv",
    "accounts",
    "tags",
    "oauth2_provider",
    "social_django",
    "rest_framework_social_oauth2",
    "django.contrib.humanize",
    "graphene_django",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # <-- add to load language prefix
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "jobs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ]
        },
    }
]

WSGI_APPLICATION = "jobs.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")},
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'ghuyhfun',
    #     'USER': 'ghuyhfun',
    #     'PASSWORD': 'ZMp3Pi11S9RJ7DVmovpo2aPo3rYiWlm3',
    #     'HOST': 'baasu.db.elephantsql.com',
    #     'PORT': '5432',
    # }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 5}},
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

LANGUAGE_CODE = "en"

LANGUAGES = (("en", _("English")), ("bn", _("Bengali")))

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")
# ALLOWED_HOSTS = ['django-portal.herokuapp.com', 'localhost', 'jobs.manjurulhoque.com', '127.0.0.1', 'localhost:3000']
# cors config
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ["*"]

CORS_ALLOW_METHODS = ("DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT")

CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # for production
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

AUTH_USER_MODEL = "accounts.user"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework.authentication.TokenAuthentication',
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "EXCEPTION_HANDLER": "jobsapp.api.custom_exception.custom_exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "file": {
#             "level": "INFO",
#             "class": "logging.handlers.TimedRotatingFileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/debug.log"),
#             "when": "D",  # this specifies the interval
#             "interval": 1,  # defaults to 1, only necessary for other values
#             "backupCount": 100,  # how many backup file to keep, 10 days
#         }
#     },
#     "loggers": {
#         "django": {"handlers": ["file"], "level": "INFO", "propagate": True},
#         "project": {"handlers": ["file"], "level": "INFO", "propagate": True},
#         "": {"handlers": ["file"], "level": "INFO", "propagate": True},
#     },
# }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "handlers": {
        "console": {"level": "INFO", "filters": ["require_debug_true"], "class": "logging.StreamHandler"},
        "null": {"class": "logging.NullHandler"},
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"]},
        "django.request": {"handlers": ["mail_admins"], "level": "ERROR", "propagate": False},
        "django.security": {"handlers": ["mail_admins"], "level": "ERROR", "propagate": False},
        "py.warnings": {"handlers": ["console"]},
    },
}

ELASTIC_HOST_NAME = os.environ.get("ELASTIC_HOST_NAME", "localhost")
ELASTIC_HOST_PORT = os.environ.get("ELASTIC_HOST_PORT", "9200")
# ELASTIC_URL = os.environ.get('ELASTIC_URL', 'http://localhost:9200')


ELASTICSEARCH_DSL = {"default": {"hosts": ELASTIC_HOST_NAME + ":" + ELASTIC_HOST_PORT}}

# Documentation
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}},
    "DEFAULT_FIELD_INSPECTORS": [
        "drf_yasg.inspectors.CamelCaseJSONFilter",
        "drf_yasg.inspectors.InlineSerializerInspector",
        "drf_yasg.inspectors.RelatedFieldInspector",
        "drf_yasg.inspectors.ChoiceFieldInspector",
        "drf_yasg.inspectors.FileFieldInspector",
        "drf_yasg.inspectors.DictFieldInspector",
        "drf_yasg.inspectors.SimpleFieldInspector",
        "drf_yasg.inspectors.StringDefaultFieldInspector",
    ],
    "USE_SESSION_AUTH": False,
}

LOGIN_URL = reverse_lazy("accounts:login")
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = (
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.twitter.TwitterOAuth",
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.linkedin.LinkedinOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_GITHUB_KEY = env("SOCIAL_AUTH_GITHUB_KEY", default="")
SOCIAL_AUTH_GITHUB_SECRET = env("SOCIAL_AUTH_GITHUB_SECRET", default="")

SOCIAL_AUTH_FACEBOOK_KEY = env("SOCIAL_AUTH_FACEBOOK_KEY", default="")
SOCIAL_AUTH_FACEBOOK_SECRET = env("SOCIAL_AUTH_FACEBOOK_SECRET", default="")

SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {"fields": "id, name, email, age_range"}

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = env("SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY", default="")
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = env("SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET", default="")

SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ["r_liteprofile", "r_emailaddress"]
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ["emailAddress"]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", default="")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", default="")

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "accounts.pipeline.update_user",
)

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

GRAPHENE = {
    # package path to schema file
    "SCHEMA": "jobs.schema.schema",
    # https://docs.graphene-python.org/projects/django/en/latest/introspection/
    "SCHEMA_INDENT": 4,  # Defaults to None (displays all data on a single line)
    "MIDDLEWARE": ["graphene_django.debug.DjangoDebugMiddleware", "graphql_jwt.middleware.JSONWebTokenMiddleware"],
}

GRAPHQL_JWT = {
    # 'JWT_PAYLOAD_HANDLER': 'jobs.schema.jwt_payload',
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_EXPIRATION_DELTA": timedelta(minutes=60),
}

ENABLE_PROMETHEUS = int(os.environ.get("ENABLE_PROMETHEUS", "0"))

if ENABLE_PROMETHEUS:
    INSTALLED_APPS += ["django_prometheus"]
    MIDDLEWARE = ['django_prometheus.middleware.PrometheusBeforeMiddleware'] + MIDDLEWARE + \
                 ['django_prometheus.middleware.PrometheusAfterMiddleware']
    MIDDLEWARE.append("jobs.middlewares.CustomMiddleware")
