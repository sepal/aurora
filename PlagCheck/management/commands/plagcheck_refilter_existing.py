from django.core.management.base import BaseCommand

from PlagCheck.verification import plagcheck_filter_existing_suspicions

class Command(BaseCommand):
    help = 'Refilters all existing documents in plagcheck. Useful if filters have changed in the meantime.'

    def handle(self, *args, **options):
        plagcheck_filter_existing_suspicions()
