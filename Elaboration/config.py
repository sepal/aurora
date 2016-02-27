from django.apps import AppConfig
from django.db.models.signals import post_save
from Elaboration.models import Elaboration
from PlagCheck import tasks


# gets executed when a elaboration gets saved (created/updated)
# and triggers the PlagCheck task.
def post_save_elaboration_callback(sender, **kwargs):
    doc = kwargs['instance']

    data = doc.elaboration_text
    if len(data) > 5:
        handle = tasks.check.delay(doc=data,
                                   doc_id=doc.id)

# custom AppConfig class to register the post_save handler after django has initialized
# the system
class ElaborationConfig(AppConfig):

    name = "Elaboration"

    def ready(self):
        # install post_save_elaboration_callback
        post_save.connect(post_save_elaboration_callback, sender=Elaboration)