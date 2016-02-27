from django.core.management.base import BaseCommand
from django.db import connection

from PlagCheck.models import *


class Command(BaseCommand):
    help = 'Populates database with demo data'

    def handle(self, *args, **options):
        clear_plagcheck_but_filtered()


def clear_plagcheck_but_filtered():
    cursor = connection.cursor()

    cursor.execute(
        'DELETE '
        'FROM Plagcheck_reference '
        'WHERE doc_id NOT IN ('
            'SELECT doc_id '
            'FROM Plagcheck_suspect '
            'WHERE state = %s)', [SuspectState.FILTER.value])

    cursor.execute(
        'DELETE '
        'FROM Elaboration_elaboration '
        'WHERE id NOT IN ('
            'SELECT doc_id '
            'FROM Plagcheck_reference'
        ')'
    )

    cursor.execute(
        'DELETE '
        'FROM Plagcheck_result '
        'WHERE id NOT IN ('
            'SELECT result_id '
            'FROM Plagcheck_suspect '
            'WHERE state = %s)', [SuspectState.FILTER.value])

    cursor.execute(
        'DELETE '
        'FROM Plagcheck_suspect '
        'WHERE state != %s', [SuspectState.FILTER.value])
