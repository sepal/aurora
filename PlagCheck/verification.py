from django.core.exceptions import ObjectDoesNotExist
from PlagCheck.models import Store

from PlagCheck import tasks as plagcheck_tasks


def plagcheck_store_and_verify(**kwargs):
    doc = plagcheck_store(**kwargs)

    plagcheck_verify(doc)

    return doc


def plagcheck_verify(doc):
    if doc:
        plagcheck_tasks.check.delay(doc_id=doc.id)


def plagcheck_check_unverified():
    unverified_docs = Store.get_unverified_docs()

    print("Got {0} unverified documents.".format(len(unverified_docs)))

    for doc in unverified_docs:
        plagcheck_verify(doc)


def plagcheck_store(**kwargs):
    doc = None

    if kwargs['submission_time'] is None:
        return doc

    try:
        doc = Store.objects.get(
            elaboration_id=kwargs['elaboration_id'],
            user_id=kwargs['user_id'],
            is_revised=kwargs['is_revised'],
        )

        # skip verification if latest version already stored
        if str(doc.submission_time) == str(kwargs['submission_time']):
            return None

        updated_doc = Store(pk=doc.pk, **kwargs)
        updated_doc.save()

        doc = updated_doc

    except ObjectDoesNotExist:
        doc = Store.objects.create(**kwargs)

    return doc


def plagcheck_elaboration(elaboration, is_revised=False, store_only=False):

        text = elaboration.elaboration_text
        if is_revised:
            text = elaboration.revised_elaboration_text

        username = elaboration.user.matriculation_number
        if username is None:
            username = elaboration.user.nickname

        if not store_only:
            doc = plagcheck_store_and_verify(
                text=text,
                elaboration_id=elaboration.id,
                user_id=elaboration.user.id,
                user_name=username,
                submission_time=str(elaboration.submission_time),
                is_revised=is_revised,
            )
        else:
            doc = plagcheck_store(
                text=text,
                elaboration_id=elaboration.id,
                user_id=elaboration.user.id,
                user_name=username,
                submission_time=str(elaboration.submission_time),
                is_revised=is_revised,
            )

        return doc
