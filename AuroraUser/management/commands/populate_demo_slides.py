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
    lecturs = ['2017-03-11','2017-03-18','2017-03-25','2017-04-01','2017-04-08','2017-04-13','2017-04-22','2017-05-02','2017-05-16','2017-05-24','2017-05-31']
    subjcts = ['E-Voting','History','Critical Thinking','Pre-Scientific Thinking','Computational Thinking','Computers in Society','Intelligence','Surveillance','Bias','Privacy']
    snams = ['Abibliophobia','Absquatulate','Allegator','Anencephalous','Argle-bargle','Batrachomyomachy','Billingsgate','Bloviate','Blunderbuss','Borborygm','Boustrophedon','Bowyang','Brouhaha','Bumbershoot','Callipygian','Canoodle','Cantankerous','Catercornered','Cockalorum','Cockamamie','Codswallop','Collop','Collywobbles','Comeuppance','Crapulence','Crudivore','Discombobulate','Donnybrook','Doozy','Dudgeon','Ecdysiast','Eructation','Fard','Fartlek','Fatuous','Filibuster','Firkin','Flibbertigibbet','Flummox','Folderol','Formication','Fuddy-duddy','Furbelow','Furphy','Gaberlunzie','Gardyloo!','Gastromancy','Gazump','Gobbledygook','Gobemouche','Godwottery','Gongoozle','Gonzo','Goombah','Hemidemisemiquaver','Hobbledehoy','Hocus-pocus','Hoosegow','Hootenanny','Jackanapes','Kerfuffle','Klutz','La-di-da','Lagopodous','Lickety-split','Lickspittle','Logorrhea','Lollygag','Malarkey','Maverick','Mollycoddle','Mugwump','Mumpsimus','Namby-pamby','Nincompoop','Oocephalus','Ornery','Pandiculation','Panjandrum','Pettifogger','Pratfall','Quean','Rambunctious','Ranivorous','Rigmarole','Shenanigan','Sialoquent','Skedaddle','Skullduggery','Slangwhanger','Smellfungus','Snickersnee','Snollygoster','Snool','Tatterdemalion','Troglodyte','Turdiform','Unremacadamized','Vomitory','Wabbit','Widdershins','Yahoo']
    for x in range(1, 9):
        tit = 'Stack %s' % x
        ta = 'tag %s' % x
        cat = 'Lecture_%s, Lecture_%s, Lecture_%s, Subject_%s, Subject_%s' % (
            lecturs[x], lecturs[x + 1], lecturs[x + 2], subjcts[x], subjcts[x + 1])
        co = Course.objects.get(short_title='gsi')
        SlideStack.objects.create(title=tit, tags=ta, categories=cat, pub_date='2017-02-14 11:35', course=co)
        for y in range(1, 15):
            t = snams[random.randint(1,100)]
            if random.randint(1,2)==1:
                t = t + ' ' + snams[random.randint(1,100)]
            im = 'vo20160614_%s.jpg' % random.randint(1, 64)
            pa = os.path.join(STATIC_ROOT, 'img/demo-slides/%s' % im)
            Slide.objects.create(title=t, slide_stack=SlideStack.objects.last())
            Slide.objects.last().image.save(im, File(open(pa, 'rb')))

    print('complete adding sample slides')
