import logging

import base64
import json
import os

from django.core.management.commands import makemessages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

# Sentinel objects that are distinct from None
_NOT_SET = object()


class Misconfiguration(Exception):
    """Exception that is raised when something is misconfigured in this file."""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "", "..")
)

SOURCE_COMMIT = os.environ.get("SOURCE_COMMIT", "unknown")

# Many of the settings are dependent on the environment we're running in.
# The default environment is development, so the programmer doesn't have to set anything
DJANGO_ENV = os.environ.get("DJANGO_ENV", "development")
_environments = ["production", "staging", "testing", "development"]
if DJANGO_ENV not in _environments:
    raise Misconfiguration(f"Set DJANGO_ENV to one of: {', '.join(_environments)}")


def _set_django_env(env):
    """Set the DJANGO_ENV variable.
    This is a helper function for the doctests below because doctests cannot set global variables.
    """
    # pylint: disable=global-statement
    global DJANGO_ENV
    DJANGO_ENV = env


def setting(*, development, production, staging=_NOT_SET, testing=_NOT_SET):
    """Generate a setting depending on the DJANGO_ENV and the arguments.
    This function is meant for static settings that depend on the DJANGO_ENV. If the
    staging or testing arguments are left to their defaults, they will fall back to
    the production and development settings respectively.
    Example:
        >>> _set_django_env("production")
        >>> SEND_MESSAGES_WITH = setting(development="console", production="mail", staging="DM")
        >>> SEND_MESSAGES_WITH
        'mail'
        >>> _set_django_env("testing")
        >>> setting(development="console", production="mail", staging="DM")
        'console'
    """
    if DJANGO_ENV == "development" or (DJANGO_ENV == "testing" and testing is _NOT_SET):
        return development
    if DJANGO_ENV == "testing":
        return testing
    if DJANGO_ENV == "production" or (DJANGO_ENV == "staging" and staging is _NOT_SET):
        return production
    if DJANGO_ENV == "staging":
        return staging
    raise Misconfiguration(f"Set DJANGO_ENV to one of: {', '.join(_environments)}")


def from_env(
    name, *, production=_NOT_SET, staging=_NOT_SET, testing=_NOT_SET, development=None
):
    """Generate a setting that's overridable by the process environment.
    This will raise an exception if a default is not set for production. Because we use
    the sentinel value _NOT_SET, you can still set a default of None for production if wanted.
    As with :func:`setting` the staging and testing values will fall back to production
    and development. So if an environment variable is required in production, and no default
    is set for staging, staging will also raise the exception.
    Example:
        >>> _set_django_env("production")
        >>> # A secret key should always be set in production via the environment
        >>> from_env("MEDIA_ROOT", development="/media/root")
        Traceback (most recent call last):
          ...
        thaliawebsite.settings.Misconfiguration: Environment variable `MEDIA_ROOT` must be supplied in production
        >>> _set_django_env("development")
        >>> from_env("MEDIA_ROOT", development="/media/root")
        '/media/root'
    """
    try:
        return os.environ[name]
    except KeyError:
        if DJANGO_ENV == "production" or (
            DJANGO_ENV == "staging" and staging is _NOT_SET
        ):
            if production is _NOT_SET and os.environ.get("MANAGE_PY", "0") == "0":
                # pylint: disable=raise-missing-from
                raise Misconfiguration(
                    f"Environment variable `{name}` must be supplied in production"
                )
            if production is _NOT_SET and os.environ.get("MANAGE_PY", "0") == "1":
                logger.warning(
                    "Ignoring unset %s because we're running a management command", name
                )
                return development
            return production
        if DJANGO_ENV == "staging":
            return staging
        if DJANGO_ENV == "development" or (
            DJANGO_ENV == "testing" and testing is _NOT_SET
        ):
            return development
        if DJANGO_ENV == "testing":
            return testing


###############################################################################
# Site settings

# We use this setting to generate the email addresses
SITE_DOMAIN = from_env(
    "SITE_DOMAIN", development="bingo.localhost", production="bingo.nsvvheyendaal.nl"
)
# We use this domain to generate some absolute urls when we don't have access to a request
BASE_URL = os.environ.get("BASE_URL", f"https://{SITE_DOMAIN}")

# Default FROM email
DEFAULT_FROM_EMAIL = f"{os.environ.get('ADDRESS_NOREPLY', 'noreply')}@nsvvheyendaal.nl"
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = DEFAULT_FROM_EMAIL

###############################################################################
# Django settings

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = from_env(
    "SECRET_KEY", development="#o-0d1q5&^&06tn@8pr1f(n3$crafd++^%sacao7hj*ea@c)^t"
)

ZOOM_LINK = from_env("ZOOM_LINK", development="https://zoom.example")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    SITE_DOMAIN,
    *from_env("ALLOWED_HOSTS", development="*", production="").split(","),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#internal-ips
INTERNAL_IPS = setting(development=["127.0.0.1", "172.25.44.66", "*"], production=[])

# https://django-compressor.readthedocs.io/en/stable/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = setting(development=False, production=True)

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = from_env("STATIC_ROOT", development=os.path.join(BASE_DIR, "static"))

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SENDFILE_BACKEND = setting(
    development="django_sendfile.backends.development",
    production="django_sendfile.backends.nginx",
)
# https://github.com/johnsensible/django-sendfile#nginx-backend
SENDFILE_URL = "/media/sendfile/"
SENDFILE_ROOT = from_env("SENDFILE_ROOT", production="/concrexit/media/")

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = from_env("MEDIA_ROOT", development=os.path.join(BASE_DIR, "media"))

# https://docs.djangoproject.com/en/dev/ref/settings/#conn-max-age
CONN_MAX_AGE = int(from_env("CONN_MAX_AGE", development="0", production="60"))

# Useful for managing members
# https://docs.djangoproject.com/en/dev/ref/settings/#data-upload-max-number-fields
DATA_UPLOAD_MAX_NUMBER_FIELDS = os.environ.get("DATA_UPLOAD_MAX_NUMBER_FIELDS", 10000)

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = setting(development=True, production=False, testing=False)

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = setting(development=False, production=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = setting(development=False, production=True)

###############################################################################
# Email settings
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
_EMAIL_BACKEND = from_env("EMAIL_BACKEND", development="console", production="smtp")
if _EMAIL_BACKEND == "console":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if _EMAIL_BACKEND == "smtp":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST")
    EMAIL_PORT = os.environ.get("DJANGO_EMAIL_PORT", 25)
    EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = os.environ.get("DJANGO_EMAIL_USE_TLS", "1") == "1"
    EMAIL_TIMEOUT = int(os.environ.get("EMAIL_TIMEOUT", "10"))
    if EMAIL_HOST is None:
        logger.warning(
            "The email host is set to the default of localhost, are you sure you don't want to set EMAIL_HOST?"
        )
        EMAIL_HOST = "localhost"

###############################################################################
# Database settings
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASE_ENGINE = from_env(
    "DATABASE_ENGINE", development="sqlite", production="postgresql", testing=None
)
if DATABASE_ENGINE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

if DATABASE_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "USER": os.environ.get("POSTGRES_USER", "concrexit"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", None),
            "NAME": os.environ.get("POSTGRES_DB", ""),
            "HOST": os.environ.get("POSTGRES_HOST", ""),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }

if DJANGO_ENV == "testing":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "thalia",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "postgres",
            "PORT": 5432,
        },
    }

###############################################################################
# (Mostly) static settings
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.admin",
    # Dependencies
    "import_export",
    "bootstrap4",
    "compressor",
    "debug_toolbar",
    # Our apps
    "game",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

if DJANGO_ENV == "testing":
    for x in (
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "django.middleware.http.ConditionalGetMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
    ):
        MIDDLEWARE.remove(x)
    for x in ("debug_toolbar",):
        INSTALLED_APPS.remove(x)

ROOT_URLCONF = "bingo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": setting(development=True, production=False),
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

if DJANGO_ENV in ["production", "staging"]:
    # Use caching template loader
    TEMPLATES[0]["OPTIONS"]["loaders"] = [
        (
            "django.template.loaders.cached.Loader",
            [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        )
    ]

    # Default logging: https://github.com/django/django/blob/master/django/utils/log.py
    # We disable mailing the admin.
    # Server errors will be sent to Sentry via the config below this.
    LOGGING = {
        "version": 1,
        "formatters": {
            "verbose": {"format": "%(asctime)s %(name)s[%(levelname)s]: %(message)s"},
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            }
        },
        "loggers": {
            "django": {"handlers": [], "level": "INFO"},
            "": {"handlers": ["console"], "level": "INFO"},
        },
    }

WSGI_APPLICATION = "bingo.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth."
            "password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
    },
]

PASSWORD_HASHERS = setting(
    development=(
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ),
    production=(
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
        "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
        "django.contrib.auth.hashers.BCryptPasswordHasher",
    ),
    testing=("django.contrib.auth.hashers.MD5PasswordHasher",),
)

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "nl"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Static files
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders
    "compressor.finders.CompressorFinder",
)

# Compressor settings
COMPRESS_ENABLED = True

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ]
}

BOOTSTRAP4 = {"required_css_class": "required-field"}
