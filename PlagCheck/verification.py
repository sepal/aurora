from django.core.exceptions import ObjectDoesNotExist

from PlagCheck.models import Document, Suspicion, SuspicionState
from PlagCheck.util.filter import filter_suspicion, load_suspicion_filters
from PlagCheck import tasks as plagcheck_tasks


def plagcheck_store_and_verify(store_only=False, dry=False, **kwargs):
    doc = plagcheck_store(dry, **kwargs)

    if not store_only:
        plagcheck_verify(doc)

    return doc


def plagcheck_verify(doc):
    if doc:
        plagcheck_tasks.check.delay(doc_id=doc.id)


def plagcheck_check_unverified():
    unverified_docs = Document.get_unverified_docs()

    print("Got {0} unverified documents.".format(len(unverified_docs)))

    for doc in unverified_docs:
        plagcheck_verify(doc)


def plagcheck_store(dry_run=False, **kwargs):
    doc = None

    if kwargs['submission_time'] in (None, 'None'):
        return None

    try:
        doc = Document.objects.get(
            elaboration_id=kwargs['elaboration_id'],
            user_id=kwargs['user_id'],
            is_revised=kwargs['is_revised'],
        )

        # skip verification if latest version already stored
        if str(doc.submission_time) == str(kwargs['submission_time']):
            return None

        updated_doc = Document(pk=doc.pk, **kwargs)

        if not dry_run:
            updated_doc.save()

        doc = updated_doc

    except ObjectDoesNotExist:
        if not dry_run:
            doc = Document.objects.create(**kwargs)
        else:
            doc = object()

    return doc


def plagcheck_elaboration(elaboration, store_only=False):

        username = elaboration.user.matriculation_number
        if username is None:
            username = elaboration.user.username

        doc = plagcheck_store_and_verify(
            store_only=store_only,

            text=elaboration.elaboration_text,
            elaboration_id=elaboration.id,
            user_id=elaboration.user.id,
            user_name=username,
            submission_time=str(elaboration.submission_time),
            is_revised=False,
        )

        if elaboration.elaboration_text != elaboration.revised_elaboration_text:
            doc = plagcheck_store_and_verify(
                store_only=store_only,

                text=elaboration.revised_elaboration_text,
                elaboration_id=elaboration.id,
                user_id=elaboration.user.id,
                user_name=username,
                submission_time=str(elaboration.submission_time),
                is_revised=True,
            )

        return doc


def plagcheck_filter_existing_suspicions(dry_run=False):
    suspicions = Suspicion.objects.filter(state__exact=SuspicionState.SUSPECTED.value)

    suspicion_filters = load_suspicion_filters()

    for suspicion in suspicions:
        (new_state, reason) = filter_suspicion(suspicion, suspicion_filters)

        if suspicion.state_enum is not new_state:
            print("Change (suspicion_id: {0}) {1} to {2} by {3}".format(suspicion.id, str(suspicion.state_enum), str(new_state), reason.__name__))

            if new_state is None:
                suspicion.state = SuspicionState.FALSE_POSITIVE.value
            else:
                suspicion.state = new_state.value

            if not dry_run:
                suspicion.save()
