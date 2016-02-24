from __future__ import absolute_import

import os, time

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuroraProject.settings')

from django.conf import settings     # noqa
from django.db.utils import OperationalError

from Plagcheck.models import Reference, Result, Suspect, SuspectState # noqa
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


@app.task(bind=True)
def check(self, **kwargs):
    try:
        doc_id = kwargs['doc_id']

        # delete existing references to older versions of this document
        Reference.remove_references(doc_id)

        # generate a list of hashes
        hash_list = sherlock.signature_str(kwargs['doc'])

        # remove duplicate hashes from the list
        hash_set = set(hash_list)

        hash_count = len(hash_set)

        # check if hashes are generated which means punctuations found
        suspects = list()
        auto_filtered = False
        if hash_count > 0:
            # store (new) references
            Reference.store_references(doc_id, hash_set)

            # compute individual similarity by computing the count
            # of matches for each other document. This returns a list
            # of possible matching documents.
            similar_elaborations = Reference.get_similar_elaborations(doc_id)
            for (similar_doc_id, match_count, filter_id) in similar_elaborations:
                percent = (100.0/hash_count) * match_count

                assert(percent <= 100)

                if percent > PLAGCHECK_SIMILARITY_THRESHOLD_PERCENT:
                    if filter_id is not None:
                        auto_filtered = True

                    # put them in a list so that filtered
                    # findings can be handled later
                    suspects.append({
                        'similar_doc_id': similar_doc_id,
                        'percent': percent,
                        'filter_id': filter_id,
                        'match_count': match_count
                    })

        result = Result.objects.create(
            hash_count=hash_count,
            doc_id=doc_id,
        )

        # if there is a similar document that was assigned the state
        # FILTER then mark all suspecting elaborations as AUTO_FILTERED
        state = Suspect.DEFAULT_STATE.value
        if auto_filtered:
            state = SuspectState.AUTO_FILTERED.value

        for suspect in suspects:
            Suspect.objects.create(
                doc_id=doc_id,
                similar_to_id=suspect['similar_doc_id'],
                percent=suspect['percent'],
                match_count=suspect['match_count'],
                result=result,
                state=state
            )

        return result.celery_result()
    except OperationalError as e:
        print("Got an OperationalError, retrying")
        self.retry(exc=e, max_retries=2)
