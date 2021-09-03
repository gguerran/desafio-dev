from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='SECRET_KEY_NOT_GOOD')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps de terceiros
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'oauth2_provider',
    # Apps locais
    'desafio_dev.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]

ROOT_URLCONF = 'desafio_dev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom context processors
                'desafio_dev.core.context_processors.stores',
            ],
        },
    },
]

WSGI_APPLICATION = 'desafio_dev.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": config("SQL_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("SQL_DATABASE", default="github-actions"),
        "USER": config("SQL_USER", default="postgres"),
        "PASSWORD": config("SQL_PASSWORD", default="postgres"),
        "HOST": config("SQL_HOST", default="localhost"),
        "PORT": config("SQL_PORT", default=5432),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', 'oauth2_provider.backends.OAuth2Backend']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['oauth2_provider.contrib.rest_framework.OAuth2Authentication'],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 300,
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'},
}

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
