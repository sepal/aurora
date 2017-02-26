from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuroraProject.settings')

from django.conf import settings
from django.db.utils import OperationalError

from AuroraUser.models import AuroraUser
app = Celery('AuroraProject')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def calculate_review_karma(self, **kwargs):
    user_id = kwargs['user_id']
    user = AuroraUser.objects.get(id=kwargs['user_id'])
    return user.calculate_review_karma
