"""
Django settings for secretaria_salud project.
Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key .env when deploying to production!!!! (TODO)
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'https://secretaria-salud.herokuapp.com', 'https://secretaria-salud.herokuapp.com/', 'secretaria-salud.herokuapp.com']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',


    # Third Pary Apps
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',
    'simple_history',
    'django_filters',
    'sslserver',
    'tailwind',
    'secretariasalud',
    # Django Project Apps
    'dashboard',
    # 'apps.users',
    'core',
    # 'django_browser_reload',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    # "django_browser_reload.middleware.BrowserReloadMiddleware",
]


ROOT_URLCONF = 'secretaria_salud.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'notifications.context_processors.notifications'
            ],
        },
    },
]


WSGI_APPLICATION = 'secretaria_salud.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# SECURITY WARNING: keep the DB credentials hidden in .env when deploying to production!!!! (TODO)
DATABASES = {
    'default': {
        'ENGINE': os.getenv('SQL_ENGINE'),
        'NAME': os.getenv('SQL_DBNAME'),
        'USER': os.getenv('SQL_USER'),
        'PASSWORD': os.getenv('SQL_PASSWORD'),
        'HOST': os.getenv('SQL_HOST'),
        'Port': os.getenv('SQL_PORT'),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = 'en-us' #Mexico: es-mx
TIME_ZONE = 'UTC' # Mexico city: America/Mexico_City || Hermosillo: America/Hermosillo
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "secretariasalud/static",
]
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATA_UPLOAD_MAX_MEMORY_SIZE=10*1024*1024

# Third Party Apps' Dependencies
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'


LOGIN_URL = '/'

LOGIN_REDIRECT_URL = 'dashboard:index'

# Set default user model
AUTH_USER_MODEL = 'users.User'

# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

TAILWIND_APP_NAME = 'secretariasalud'

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

NPM_BIN_PATH = '/usr/bin/npm'

AUTH_USER_MODEL = 'core.Usuario'


# Configure cors headers
CORS_ORIGIN_ALLOW_ALL = True
# Change when it is needed


LOGOUT_REDIRECT_URL = '/'
