from django.apps import AppConfig
from django.db.models.signals import post_save
from Elaboration.models import Elaboration
from Plagcheck import tasks


# gets executed when a elaboration gets saved (created/updated)
# and triggers the Plagcheck task.
def post_save_elaboration_callback(sender, **kwargs):
    print("post_save_elaboration_callback")

    doc = kwargs['instance']

    data = doc.elaboration_text

    handle = tasks.check.delay(data, doc.id, 0, "default", "test", kwargs['created'])

# custom AppConfig class to register the post_save handler after django has initialized
# the system
class ElaborationConfig(AppConfig):

    name = "Elaboration"

    def ready(self):
        print("Install post_save_elaboration_callback")
        post_save.connect(post_save_elaboration_callback, sender=Elaboration)