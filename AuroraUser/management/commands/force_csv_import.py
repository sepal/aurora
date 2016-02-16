from django.core.management.base import BaseCommand
import time
from Plagcheck import tasks

class Command(BaseCommand):
    help = 'Populates database with demo data'

    def handle(self, *args, **options):
        if len(args) < 1:
            print("usage: force_csv_import CSV_FILE")
            exit(1)
        force_csv_import(args[0])

def force_csv_import(csv_file):
    imported = list()
    i = 0
    try:
        with open(csv_file, "r") as f:
            for line in f:
                # skip column headers
                if i is 0:
                    print("Headers: %s" % line)
                    i += 1
                    continue

                data = line.split(',')
                try:
                    new = dict()
                    new['id'] = int(data[0])
                    new['challange'] = data[1]
                    new['user'] = data[2]
                    # eg. 2015-03-30 13:51:05.880115
                    new['created'] = time.strptime(data[3], "%Y-%m-%d %H:%M:%S.%f")
                    new['submitted'] = time.strptime(data[4], "%Y-%m-%d %H:%M:%S.%f")
                    new['text'] = ",".join(data[5:])
                except (IndexError, ValueError) as e:
                    try:
                        old = imported[-1]
                        old['text'] += line
                        continue
                    except Exception as e:
                        print("Error on line: %s" % line)
                        continue
                        #raise e

                imported.append(new)
    except IOError:
        print("File %s not found" % csv_file)
        exit(1)

    #print(imported)

    print("submitting %i elaborations" % len(imported))

    for elab in imported:
        tasks.check.delay(doc=elab['text'],
                          doc_id=elab['id'],
                          doc_version=0,
                          doc_type="default",
                          username="test",
                          is_new=True)
