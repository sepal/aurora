from sys import stdout

from django.core.management.base import BaseCommand

from PlagCheck.verification import plagcheck_filter_existing_suspicions

class Command(BaseCommand):
    help = 'Triggers a plagiarism check for documents which haven\'t checked yet'

    def handle(self, *args, **options):
        plagcheck_filter_existing_suspicions()
