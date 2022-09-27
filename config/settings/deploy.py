from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']
WSGI_APPLICATION = 'config.wsgi.deploy.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': '5432',
    }
}
