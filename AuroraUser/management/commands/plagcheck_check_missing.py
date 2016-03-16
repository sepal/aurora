from django.core.management.base import BaseCommand
from django.db import connections
import PlagCheck
from AuroraProject.settings import PLAGCHECK_DATABASE
from Elaboration.models import Elaboration

from PlagCheck.models import *


class Command(BaseCommand):
    help = 'Triggers a plagiarism check for documents which haven\'t checked yet'

    def handle(self, *args, **options):
        #cursor = connections[PLAGCHECK_DATABASE].cursor()

        #cursor.execute(
        #    'SELECT id, elaboration_text '
        #    'FROM Elaboration_elaboration '
        #    'WHERE id NOT IN ('
        #        'SELECT doc_id '
        #        'FROM Plagcheck_result) '
        #    'ORDER BY submission_time ASC')
        elaborations = Elaboration.objects.all()
        for elab in elaborations:
            PlagCheck.tasks.check.delay(doc_id=elab.id, doc=elab.elaboration_text)

        #for row in cursor.fetchall():
        #    PlagCheck.tasks.check.delay(doc_id=row[0], doc=row[1])
