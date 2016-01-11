from __future__ import absolute_import

import os, time

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuroraProject.settings')

from django.conf import settings     # noqa

from Plagcheck.models import Reference, Result, Elaboration # noqa
import sherlock # noqa

app = Celery('AuroraProject')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task()
def check(doc, doc_id, doc_version, doc_type, username, is_new):

    # delete existing references to older versions of this document
    if is_new is False:
        Reference.del_ref(doc_id)

    # generate a list of hashes
    hash_list = sherlock.signature_str(doc)

    # check if hashes are generated which means punctuations found
    overall_percentage = 0
    if len(hash_list) > 0:
        # store (new) references
        Reference.store(hash_list, doc_id)

        # check for equal hashes
        same_hashes = Reference.get_matching_count(doc_id)

        overall_percentage = (100.0/len(hash_list)) * same_hashes

    result = Result.objects.create(overall_percentage=overall_percentage,
                                   hash_count=len(hash_list),
                                   doc_id=doc_id,
                                   doc_version=doc_version,
                                   doc_type=doc_type,
                                   username=username)

    return result.celery_result()
