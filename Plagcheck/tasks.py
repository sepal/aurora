from __future__ import absolute_import

import os, time

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuroraProject.settings')

from django.conf import settings  # noqa
from Plagcheck.models import Reference, Result, Elaboration
import sherlock

app = Celery('AuroraProject')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

    with open("/tmp/test.txt", 'w') as f:
        test = ("this is a test %s" % time.strftime("%H:%M:%S"))
        f.write(test)
        print(test)
        time.sleep(2)

    return dict(result="Success", selse=None, test=self.request)


@app.task()
def check(doc, doc_id, doc_version, doc_type, username, is_new):

    if is_new is False:
        try:
            Reference.objects.filter(doc_id=doc_id).delete()
        except Reference.DoesNotExist:
            pass

    with open("/tmp/file.txt", 'w') as f:
        f.write(doc)

    hash_list = sherlock.signature("/tmp/file.txt")

    # check for equal signatures
    same_hashes = 0
    for _hash in hash_list:
        hash = str(_hash)
        try:
            Reference.objects.get(hash=hash)
            same_hashes += 1
        except Reference.MultipleObjectsReturned as e:
            pass
        except Reference.DoesNotExist as e:
            pass

    try:
        overall_p = (100.0/len(hash_list)) * same_hashes
    except ZeroDivisionError as e:
        overall_p = -1

    # create references
    for _hash in hash_list:
        hash = str(_hash)
        Reference.objects.create(hash=hash, doc_id=doc_id)

    result = Result.objects.create(overall_p=overall_p,
                                   hash_count=len(hash_list),
                                   doc_id=doc_id,
                                   doc_version=doc_version,
                                   doc_type=doc_type,
                                   username=username)

    return result.celery_result()
