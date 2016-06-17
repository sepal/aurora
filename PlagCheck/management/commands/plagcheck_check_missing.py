from django.core.management.base import BaseCommand

from PlagCheck.verification import plagcheck_elaboration, plagcheck_check_unverified
from Elaboration.models import Elaboration

class Command(BaseCommand):
    help = 'Triggers a plagiarism check for documents which haven\'t checked yet'

    def handle(self, *args, **options):

        elaborations = Elaboration.objects.all().order_by('submission_time')
        for elab in elaborations:

            plagcheck_elaboration(elab, store_only=True)

        plagcheck_check_unverified()
