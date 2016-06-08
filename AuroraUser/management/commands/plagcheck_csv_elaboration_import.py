from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
import time
from Challenge.models import Challenge
from AuroraUser.models import AuroraUser
from Elaboration.models import Elaboration
from django.core.exceptions import ObjectDoesNotExist
import argparse
from PlagCheck import tasks


class Command(BaseCommand):
    help = 'Populates database with demo data'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    def handle(self, *args, **options):
        force_csv_import(options['csv'])

def readlines(f):
    line = []
    while True:
        s = f.read(1)
        if len(s) == 0:
            if len(line) > 0:
                yield line
            return
        if s == b'\r':
            t = f.read(1)
            if t == b'\n':
                if len(line) > 0:
                    yield line
                line = []
            else:
                line.append(t)
        else:
            line.append(s)

def add_elaboration(elab, challenge):

    #if is_revised:
    #    text = self.revised_elaboration_text

    #if self.user.matriculation_number is None:
    #    self.user.matriculation_number = str(self.user_id)


    tasks.check.delay(
        text=elab['text'],
        elaboration_id=elab['id'],
        user_id=0,
        user_name=elab['user'],
        # submission_time=time.strftime('%Y-%m-%dT%H:%M:%SZ', elab['submitted']),
        submission_time=elab['submitted'],
        is_revised=False,
    )


def force_csv_import(csv_file, begin_at=0):
    i = 0

    default_challenge = Challenge.objects.all()[0]
    with open(csv_file, "rb") as f:
        for bytelist in readlines(f):

            line = b''.join(bytelist).decode("utf-8")

            # skip first begin_at lines
            # line with index 0 is always skipped, because it contains just
            # column names
            if i <= begin_at:
                i += 1
                continue

            i += 1
            data = line.split(',', 5)
            try:
                elab = dict()
                elab['id'] = int(data[0])
                elab['challange'] = data[1]
                elab['user'] = data[2]
                # eg. 2015-03-30 13:51:05.880115
                elab['created'] = time.strptime(data[3], "%Y-%m-%d %H:%M:%S.%f")

                if 'None' in data[4]:
                    elab['submitted'] = None
                else:
                    try:
                        elab['submitted'] = time.strptime(data[4], "%Y-%m-%d %H:%M:%S.%f")
                        elab['submitted'] = data[4]
                    except ValueError:
                        elab['submitted'] = time.strptime(data[4], "%Y-%m-%d %H:%M:%S")
                        elab['submitted'] = data[4]

                elab['text'] = data[5]
            except (IndexError, ValueError) as e:
                print(data)
                raise ValueError("Error on line(%i): %s" % (i, line), e)
            done = False
            while done is False:
                try:
                    add_elaboration(elab, default_challenge)
                    done = True

                # retry when database is locked
                except OperationalError as e:
                    pass
                except Exception as e:
                    raise Exception("Exception occurred at line %i" % i, e)
