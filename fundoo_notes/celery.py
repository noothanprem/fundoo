from celery import Celery
from fundoo_notes import settings
import os

# Setting the Default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fundoo_notes.settings')
app=Celery('fundoo_notes')

# Using a String here means the worker will always find the configuration information
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))