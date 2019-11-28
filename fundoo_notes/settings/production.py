from .base import *
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR,"Base directoryy")
DEBUG =True

load_dotenv(find_dotenv())

env_path = Path('.') / '.env'

CORS_ORIGIN_ALLOW_ALL = False




DATABASES = {
                       'default': {
                       'ENGINE': 'django.db.backends.mysql',
                       'NAME': 'noothan',  # need to replace with .env credentials stored for db
                       'USER': 'noothan',  # need to replace with .env credentials stored for db
                       'PASSWORD': 'noothan',  # need to replace with .env credentials stored for db
                       'HOST': 'localhost',  # need to replace with .env credentials stored for db
                       'PORT': '',  # need to replace with .env credentials stored for db
}
}


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/', # need to replace with .env credentials stored for db
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api-key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' # env based folder bucket settings.

SOCIAL_AUTH_GITHUB_KEY = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
# EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/note/noteshare'
SOCIAL_AUTH_EMAIL_REQUIRED = True
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']
ACCOUNT_EMAIL_REQUIRED = True



Token=os.getenv('Token')
BASE_URL=os.getenv('BASE_URL')
TEST_TOKEN=os.getenv('TEST_TOKEN')

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

#CELERY_BROKER_URL = 'amqp://localhost'
#CELERY_RESULT_BACKEND = "amqp"
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_AMOP_TASK_RESULT_EXPIRES = 1000

# For RabbitMQ
BROKER_URL = 'amqp://[ipaddress]'
CELERY_RESULT_BACKEND = 'amqp://[ipaddress]'
# Celery Data Format
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'