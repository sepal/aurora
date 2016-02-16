from __future__ import absolute_import

import os, time

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuroraProject.settings')

from django.conf import settings     # noqa

from Plagcheck.models import Reference, Result, Suspect, Elaboration # noqa
from AuroraProject.settings import PLAGCHECK_SIMILARITY_THRESHOLD_PERCENT
import sherlock # noqa

app = Celery('AuroraProject')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


class PlagcheckError(Exception):
    def __init__(self, msg):
        self.msg = msg


@app.task()
def check(**kwargs):
    doc_id = kwargs['doc_id']

    # delete existing references to older versions of this document
    if kwargs['is_new'] is False:
        Reference.del_ref(doc_id)

    # generate a list of hashes
    hash_list = sherlock.signature_str(kwargs['doc'])

    hash_count = len(hash_list)

    # check if hashes are generated which means punctuations found
    ovl_similarity = 0
    match_count = 0
    similarities = list()
    if hash_count > 0:
        # store (new) references
        Reference.store(hash_list, doc_id)

        # compute overall similarity by checking how many hashes
        # inserted for the last document match those which are
        # already in the database.
        match_count = Reference.get_match_count(doc_id)
        assert(match_count <= hash_count)
        ovl_similarity = (100.0/hash_count) * match_count
        assert(ovl_similarity <= 100)

        # compute single similarity by computing the count
        # of matches for each other document. This returns a list
        # of possible matching documents.
        similar_elaborations = Reference.get_similar_elaborations(doc_id)
        for (similar_doc_id, match_count) in similar_elaborations:
            percent = (100.0/hash_count) * match_count
            assert(percent <= 100)
            similarities.append((similar_doc_id, percent))

    result = Result.objects.create(similarity=ovl_similarity,
                                   hash_count=len(hash_list),
                                   doc_id=doc_id,
                                   doc_version=kwargs['doc_version'],
                                   doc_type=kwargs['doc_type'],
                                   username=kwargs['username'],
                                   match_count=match_count)

    for (similar_doc_id, percent) in similarities:
        if percent > PLAGCHECK_SIMILARITY_THRESHOLD_PERCENT:
            Suspect.objects.create(doc_id=doc_id, similar_to_id=similar_doc_id, percent=percent, result=result)

    return result.celery_result()
