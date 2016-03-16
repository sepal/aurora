from django.core.management.base import BaseCommand
from django.db import connection
import PlagCheck

from PlagCheck.models import *


class Command(BaseCommand):
    help = 'Triggers a plagiarism check for documents which haven\'t checked yet'

    def handle(self, *args, **options):
        cursor = connection.cursor()

        cursor.execute(
            'SELECT id, elaboration_text '
            'FROM Elaboration_elaboration '
            'WHERE id NOT IN ('
                'SELECT doc_id '
                'FROM Plagcheck_result) '
            'ORDER BY submission_time ASC')

        for row in cursor.fetchall():
            PlagCheck.tasks.check.delay(doc_id=row[0], doc=row[1])
