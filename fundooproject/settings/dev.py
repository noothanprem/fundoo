




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'noothan',
        'USER': 'noothan',
        'PASSWORD': 'noothan',
        'HOST': 'localhost',
        'PORT': '',
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


STATIC_URL = '/static/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noothanprem@gmail.com'
EMAIL_HOST_PASSWORD = 'seashore315'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
