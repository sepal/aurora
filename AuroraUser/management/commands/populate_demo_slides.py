from django.core.management.base import BaseCommand

from Slides.models import SlideStack, Slide
from Course.models import Course
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
        co = Course.objects.get(short_title='gsi')
        SlideStack.objects.create(title=tit, tags=ta, categories=cat, pub_date='2017-02-14 11:35', course=co)
        for y in range(1, 15):
            t = 'C%s, S%s' % (x, y)
            im = 'vo20160614_%s.jpg' % random.randint(1, 64)
            pa = os.path.join(STATIC_ROOT, 'img/demo-slides/%s' % im)
            Slide.objects.create(title=t, slide_stack=SlideStack.objects.last())
            Slide.objects.last().image.save(im, File(open(pa, 'rb')))

    print('complete adding sample slides')
