from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
import time
from Challenge.models import Challenge
from PlagCheck.verification import *
from sys import stdout


class Command(BaseCommand):
    help = 'Populates database with demo data'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    def handle(self, *args, **options):
        #force_csv_import(options['csv'])
        import_from_csv(args[0])


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


def import_from_csv(csv_file):
    print("Reading elaborations from csv file")
    elabs = read_elaborations_from_csv(csv_file)

    count_total = len(elabs)

    print("Got {0} elaborations.".format(count_total))

    print("Adding elaborations to plagcheck document store ...")

    count_valid=0
    count_invalid=0
    for elab in elabs:
        done = False
        while not done:
            try:
                doc = plagcheck_store(
                    text=elab['text'],
                    elaboration_id=elab['id'],
                    user_id=0,
                    user_name=elab['user'],
                    submission_time=elab['submitted'],
                    is_revised=False,
                )
                done = True

            except OperationalError:
                pass

        if doc:
            count_valid += 1
        else:
            count_invalid += 1

        percent = (100.0 / count_total) * (count_valid + count_invalid)

        stdout.write("\r{0:6.2f}% {1:10} valid, {2:10} invalid or already added".format(percent, count_valid, count_invalid))
        stdout.flush()

    stdout.write("\n")

    print("Checking all unverified documents ...")
    plagcheck_check_unverified()


def read_elaborations_from_csv(csv_file, begin_at=0):
    i = 0

    elaborations = []
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
                    continue
                elif data[4] is None:
                    continue
                else:
                    try:
                        elab['submitted'] = time.strptime(data[4], "%Y-%m-%d %H:%M:%S.%f")
                        elab['submitted'] = data[4]
                    except ValueError:
                        elab['submitted'] = time.strptime(data[4], "%Y-%m-%d %H:%M:%S")
                        elab['submitted'] = data[4]
                    #elab['submitted'] = str(elab['submitted'])

                elab['text'] = data[5]
            except (IndexError, ValueError) as e:
                print(data)
                raise ValueError("Error on line(%i): %s" % (i, line), e)
            done = False
            while done is False:
                try:
                    elaborations.append(elab)
                    done = True

                # retry when database is locked
                except OperationalError as e:
                    pass
                except Exception as e:
                    raise Exception("Exception occurred at line %i" % i, e)

    return elaborations
