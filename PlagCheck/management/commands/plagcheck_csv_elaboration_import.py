from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from django.core.exceptions import ValidationError
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


def import_from_csv(csv_file, dry_run=False):
    print("Reading elaborations from csv file")
    elabs = read_elaborations_from_csv(csv_file)

    count_total = len(elabs)

    print("Adding {0} elaborations to plagcheck document store.".format(count_total))

    count_valid=0
    count_invalid=0
    for elab in elabs:
        done = False

        while not done:
            try:
                doc = plagcheck_store(
                    dry_run=dry_run,

                    text=elab['text'],
                    elaboration_id=elab['id'],
                    user_id=0,
                    user_name=elab['user'],
                    submission_time=elab['submission_time'],
                    is_revised=False,
                )
                done = True

            except OperationalError:
                pass
            except ValidationError:
                doc = None
                done = True

        if doc:
            count_valid += 1
        else:
            count_invalid += 1

        percent = (100.0 / count_total) * (count_valid + count_invalid)

        stdout.write("\r{0:6.2f}% {1:10} valid, {2:10} invalid or already added".format(percent, count_valid, count_invalid))
        stdout.flush()

    stdout.write("\n")

    print("Checking all unverified documents ...")
    if not dry_run:
        plagcheck_check_unverified()


def read_elaborations_from_csv(csv_file, begin_at=0):
    i = 0

    elaborations = []
    with open(csv_file, "rb") as f:
        for bytelist in readlines(f):
            line = b''.join(bytelist).decode("utf-8")

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
                elab['created'] = data[3]
                elab['submission_time'] = data[4]
                elab['text'] = data[5]

            except (IndexError, ValueError) as e:
                print(data)
                raise ValueError("Error on line(%i): %s" % (i, line), e)

            elaborations.append(elab)

    return elaborations
