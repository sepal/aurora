from django.core.management.base import BaseCommand, CommandError

from Slides.models import SlideStack, Slide
from django.core.files import File
import random
import os
from AuroraProject.settings import STATIC_ROOT


class Command(BaseCommand):
    def handle(self, *args, **options):
        populate_demo_slides()


def populate_demo_slides():
    print('start adding sample slides')

    for x in range(1, 9):
        tit = 'Stack %s' % x
        ta = 'tag %s' % x
        cat = 'Chapter_Chapter %s, Chapter_Chapter %s, Chapter_Chapter %s, Topic_Topic %s, Topic_Topic %s' % (
            x, x + 1, x + 2, x, x + 1)
        SlideStack.objects.create(title=tit, tags=ta, categories=cat)
        for y in range(1, 6):
            t = 'C%s, S%s' % (x, y)
            im = '%s.jpg' % random.randint(1, 9)
            pa = os.path.join(STATIC_ROOT, 'img/demo-slides/%s' % im)
            Slide.objects.create(title=t, slide_stack=SlideStack.objects.last())
            Slide.objects.last().image.save(im, File(open(pa, 'rb')))

    print('complete adding sample slides')
