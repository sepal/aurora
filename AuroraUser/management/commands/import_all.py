from django.core.management.base import BaseCommand
from django.core.management import call_command
from Comments.models import Comment, CommentsConfig
from Review.models import ReviewConfig

class Command(BaseCommand):
    help = 'Populates database with demo data'

    def handle(self, *args, **options):
        import_all()


def import_all():
    """
    To import everything, there have to be some files present:
    courses are hardcoded
    tutors in /tmp/tutors.csv
    students have to be in /tmp/<coursename>.csv (i.e. bhci.csv and gsi.csv)

    when files are placed correctly call:
    python manage.py import_all
    """
    print("import all")
    print("Import Review Config")
    ReviewConfig.setup()
    print("Import Comments Config")
    CommentsConfig.setup()
    print("Comments Config Imported")
    call_command('import_courses')
    call_command('import_tutors')
    call_command('import_students')
    call_command('import_faq')
    call_command('import_chapters')