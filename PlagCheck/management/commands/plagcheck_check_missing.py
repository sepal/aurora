from sys import stdout

from django.core.management.base import BaseCommand

from PlagCheck.verification import plagcheck_elaboration, plagcheck_check_unverified
from Elaboration.models import Elaboration

class Command(BaseCommand):
    help = 'Triggers a plagiarism check for documents which haven\'t checked yet'

    def handle(self, *args, **options):

        elaborations = Elaboration.objects.all().order_by('submission_time')
        count = elaborations.count()
        counter = 0
        for elab in elaborations:
            counter += 1
            percent = (100.0 / count) * counter
            stdout.write("\rAdding elaboration {0} of {1} ({2:6.2f}%)".format(counter, count, percent))
            stdout.flush()
            plagcheck_elaboration(elab, store_only=True)
        stdout.write("\n")

        plagcheck_check_unverified()
