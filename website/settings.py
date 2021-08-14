from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
('app', os.path.join(BASE_DIR, 'app', 'static')),
)
SECRET_KEY = '_ggmc+yp7s3tu56vtue6)tq#$v55l2f&4^eqay!k4!k&b=(4)h'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'app.apps.AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'app/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'yidkdgrz',
            'USER': 'yidkdgrz',
            'PASSWORD': 'FxE7YIPpzFEc0q1ejcjT6q7YNWt0IdIO',
            'HOST': 'rogue.db.elephantsql.com',
            'PORT': '5432',
        },
        'test':{
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'kocmcqun',
            'USER': 'kocmcqun',
            'PASSWORD': 'xlVUECtgqn_e1T93fEXEaDDlLgf-Kfuw',
            'HOST': 'dumbo.db.elephantsql.com',
            'PORT': '5432',
        },
}

import sys
if 'test' in sys.argv:
    DATABASES['default'] = DATABASES['test'];

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'