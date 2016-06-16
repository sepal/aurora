from django.core.exceptions import ObjectDoesNotExist
from PlagCheck.models import Store

from PlagCheck import tasks as plagcheck_tasks


def plagcheck_store_and_verify(**kwargs):
    try:
        doc = Store.objects.get(
            elaboration_id=kwargs['elaboration_id'],
            user_id=kwargs['user_id'],
            is_revised=kwargs['is_revised'],
        )

        # skip verification if latest version already stored
        if str(doc.submission_time) == str(kwargs['submission_time']):
            return

        updated_doc = Store(pk=doc.pk, **kwargs)
        updated_doc.save()

    except ObjectDoesNotExist:
        doc = Store.objects.create(**kwargs)

    plagcheck_tasks.check.delay(doc_id=doc.id)

def plagcheck_elaboration(elaboration, is_revised=False):

        text = elaboration.elaboration_text
        if is_revised:
            text = elaboration.revised_elaboration_text

        username = elaboration.user.matriculation_number
        if username is None:
            username = elaboration.user.nickname

        # don't verify not submitted elaborations
        if elaboration.submission_time is None:
            return

        plagcheck_store_and_verify(
            text=text,
            elaboration_id=elaboration.id,
            user_id=elaboration.user.id,
            user_name=username,
            submission_time=str(elaboration.submission_time),
            is_revised=is_revised,
        )
