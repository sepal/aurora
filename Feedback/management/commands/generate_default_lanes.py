import traceback
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import transaction

from Feedback.models import Lane


class Command(BaseCommand):
    help = 'Generates the default lanes for the feedback system.'

    def handle(self, *args, **options):
        generate_default_lanes()


def generate_default_lanes():
    """
    Generates the default lanes for the kanban.
    """

    try:
        with transaction.atomic():
            print("Starting transaction")
            import_data()
    except Exception as e:
        traceback.print_exc()
        print("Caught error during transaction: %s" % e)
        print("Database has rolled back the transaction!")
    print("All Done!")


def import_data():
    lanes = [
        'New',
        'In Discussion',
        'Action Defined',
        'In Action',
        'To be deployed',
        'Deployed',
    ]

    pos = 0
    for lane_name in lanes:
        lane = Lane(
            name=lane_name,
            order=pos
        )
        lane.save()
        pos += 1