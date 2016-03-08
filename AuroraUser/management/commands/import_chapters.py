# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from Stack.models import Chapter

class Command(BaseCommand):
    help = 'Populates database with chapters'

    def handle(self, *args, **options):
        import_chapters()


def import_chapters():
    # create courses "GSI" and "HCI"
    print('adding chapters')
    chapters = [Chapter(name='BHCI Prolog/Epilog'), Chapter(name='User-centered Design + Design Basics'), Chapter(name='Methoden'),
    Chapter(name='psycholog. Grundlagen, Evaluation'), Chapter(name='Prototyping, Beyond the desktop'), Chapter(name='GSI Prolog/Epilog'),
    Chapter(name='Geschichte(n)'), Chapter(name='Privacy'), Chapter(name='Verletzlichkeit'), Chapter(name='Gestaltung und Verantwortung'),
    ]
    for c in chapters:
        c.save()
    