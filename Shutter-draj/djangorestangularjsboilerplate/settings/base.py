"""
Django settings for djangorestangularjsboilerplate project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django
# from djangorestangularjsboilerplate.models import MyUser
# import S3
# from S3 import CallingFormat

BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
SETTINGS_PATH = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5ez-ca3$ln#7@9=neiuzgo^$+7d_p%ww%pz+spjpir3xu4n22t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['shutter1.us-west-2.elasticbeanstalk.com']

CLIENT_ID = 'GwTf8YnLb4giiPa3mhEpj1MwfKN9HFUYL6yGwpXw'
CLIENT_SECRET = 'Fwb9AgayN7RN5Gn3HlwKebw2XZS2jSvMP7yZHTNs8HYyzK9l0wiaecpm8PY9DsBX7urL2w8L0UYw14j2A7bIRZqrqyeiUatvw3ccWf81bR904SMt056OAE5FUK0edqi8'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'oauth2_provider',
    'social.apps.django_app.default',
    'rest_framework_social_oauth2',
    'djangorestangularjsboilerplate',
    'djoser',
    'storages',
    'push_notifications',
)
PUSH_NOTIFICATIONS_SETTINGS = {
        "APNS_CERTIFICATE": "apns_dis.pem", 
}
MIDDLEWARE_CLASSES = (

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'djangorestangularjsboilerplate.middleware.account.AccountMiddleware', User Status middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'djangorestangularjsboilerplate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SETTINGS_PATH, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangorestangularjsboilerplate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# Logging
# thanks to http://stackoverflow.com/questions/5739830/simple-log-to-file-example-for-django-1-3

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# REST settings

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
    'PAGE_SIZE': 15,
}

AUTHENTICATION_BACKENDS = (
   'rest_framework_social_oauth2.backends.DjangoOAuth2',
   'django.contrib.auth.backends.ModelBackend',
   'social.backends.facebook.FacebookAppOAuth2',
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.google.GoogleOAuth2',
   'social.backends.email.EmailAuth',
)

SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

# AUTH_USER_MODEL = 'djangorestangularjsboilerplate.MyUser'
# SOCIAL_AUTH_USER_MODEL = 'djangorestangularjsboilerplate.MyUser'
# SOCIAL_AUTH_USER_MODEL = 'django.contrib.auth.models.User'

SOCIAL_AUTH_UID_LENGTH = 223
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 200
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 135
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '401018725235-udihlpgrtc4d1dkcdfkco63m07kn1vje.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'EqwO_eqMYBmNe8vQd8_YPmsY'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_PIPELINE = (
    #'djangorestangularjsboilerplate.pipeline.load_user',
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'djangorestangularjsboilerplate.soc_auth_email_val_fn.soc_auth_email_val_fn'
SOCIAL_AUTH_EMAIL_FORCE_EMAIL_VALIDATION = True

# djoser

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'ACTIVATION_URL': 'djoser-auth/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
}

# email setup

EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com' 
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'AKIAJJWM6SZP7UOEQXEA'
EMAIL_HOST_PASSWORD = 'Ai8iLzhkzqEwsM6CWnq/KgDbNtdXdQPdVrBKFxjOeexg'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Shutter Live <shutterliveios@gmail.com>'
EMAIL_DOMAIN= 'http://shutter.fwd.wf'
EMAIL_SITE_NAME='ShutterFly'

# local superusers: admin3, nidna88; 
# local users: gdasu@alumni.stanford.edu, eekbo
# prod users: gdasu@alumni.stanford.edu, eekbo ; info@learningdollars.com, eekbo

AWS_ACCESS_KEY_ID = 'AKIAIQ67CGTQET4R4I2Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'shutter-avatar'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
SITE_ID = 3
