# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, UserManager
from AuroraUser.models import AuroraUser
from taggit.managers import TaggableManager
from Course.models import *
from Challenge.models import *
from Elaboration.models import *
from Stack.models import *


class Command(BaseCommand):
    help = 'Set positive completion flag 2017'

    def handle(self, *args, **options):
        set_positive_completion_possible_2017()

def set_positive_completion_possible_2017():

    # der richtige kommand lautet so: hat von zwei kapiteln, die schon abgelaufen sind,
    # keine challenge abgegeben bzw hand-in ready (all reviews are in, es fehlt nur noch final task-abgabe)

    ended_chapters_gsi = [6, 7, 9, 10, 11, 12]
    ended_chapters_hci = [1, 2, 3]

    for course in Course.objects.all():
        if(course.short_title == "gsi"):
            ended_chapters = ended_chapters_gsi
        else:
            ended_chapters = ended_chapters_hci

        for user in AuroraUser.objects.filter(is_staff=False, is_superuser=False):
            finished_chapters = 0
            try:
                relation = CourseUserRelation.objects.get(user=user, course=course)
            except:
                continue

            for chapter_id in ended_chapters:
                chapter_stacks = Stack.objects.all().filter(course=course, chapter_id=chapter_id)
                finished_chapter = False

                for stack in chapter_stacks:
                    if finished_chapter == True:
                        continue

                    if user.can_enter_final_challenge_performant(stack):
                        finished_chapter = True
                        finished_chapters += 1

            failed = finished_chapters < 2
            relation.positive_completion_possible = (not failed)
            relation.save()

            if (failed):
                print("Disabled user " + str(user) + " for course " + course.short_title)

        print("Processed all users for " + course.title)
