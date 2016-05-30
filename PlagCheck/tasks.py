from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuroraProject.settings')

from django.conf import settings
from django.db.utils import OperationalError

from PlagCheck.models import Reference, Result, Suspect, SuspectState
from AuroraProject.settings import PLAGCHECK as plagcheck_settings
import sherlock

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
    """
    Do a check of a document against the hashes documents in the db.

    Call this function directly to run the check synchronously:

        tasks.check(args)

    or call this function asynchronously like:

        tasks.check.delay(args)

    to schedule a check at the celery worker process using a RabbitMQ message.

    TODO: currently the document text is required as kwargs argument!
    The reason is that it is easier to run tests.

    :param kwargs['doc_id'] -- ID of the document
    :param kwargs['doc'] -- Text of the document
    :return: Future object of this task invocation when called asynchronously,
    or the result if called synchronously.
    """
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
                similarity = (100.0/hash_count) * match_count

                assert(similarity <= 100)

                if similarity > plagcheck_settings['similarity_threshold'] and match_count > plagcheck_settings['minimal_match_count']:
                    if filter_id is not None:
                        auto_filtered = True

                    # put them in a list so that filtered
                    # findings can be handled later
                    suspects.append({
                        'similar_doc_id': similar_doc_id,
                        'similarity': similarity,
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
                similarity=suspect['similarity'],
                match_count=suspect['match_count'],
                result=result,
                state=state
            )

        return result.celery_result()
    except OperationalError as e:
        print("Got an OperationalError, retrying")
        self.retry(exc=e, max_retries=2, countdown=5)
