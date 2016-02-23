from django.apps import AppConfig
from django.db.models.signals import post_save
from Elaboration.models import Elaboration
from Plagcheck import tasks


# gets executed when a elaboration gets saved (created/updated)
# and triggers the Plagcheck task.
def post_save_elaboration_callback(sender, **kwargs):
    doc = kwargs['instance']

    data = doc.elaboration_text
    if len(data) > 5:
        handle = tasks.check.delay(doc=data,
                                   doc_id=doc.id,
                                   doc_version=0,
                                   doc_type="default_type",
                                   username="test",
                                   is_new=kwargs['created'])

# custom AppConfig class to register the post_save handler after django has initialized
# the system
class ElaborationConfig(AppConfig):

    name = "Elaboration"

    def ready(self):
        # install post_save_elaboration_callback
        post_save.connect(post_save_elaboration_callback, sender=Elaboration)