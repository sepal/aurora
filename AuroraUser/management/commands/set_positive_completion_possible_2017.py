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
    for course in Course.objects.all():
        ended_stacks = Stack.objects.all().filter(course=course, end_date__lt=date.today())
        course_chapter_ids = []

        for stack in ended_stacks:
            course_chapter_ids.append(stack.chapter_id)

        course_chapter_ids = list(set(course_chapter_ids))

        # if course.short_title == 'gsi':
        #     failed_course_tag = 'durchgefallen_gsi'
        # else:
        #     failed_course_tag = 'durchgefallen_bhci'

        for user in AuroraUser.objects.filter(is_staff=False, is_superuser=False):
            try:
                relation = CourseUserRelation.objects.get(user=user, course=course)
            except:
                continue

            chapter_failed_stacks = dict.fromkeys(course_chapter_ids, 0)
            total_failed_count = 0

            for stack in ended_stacks:
                if not user.can_enter_final_challenge_performant(stack):
                    chapter_failed_stacks[stack.chapter_id] = chapter_failed_stacks[stack.chapter_id] + 1

            for failed_count in chapter_failed_stacks.values():
                if failed_count >= 2:
                    total_failed_count += 1

            failed_course_by_tag = False
            # tags = user.tags.names()
            # if failed_course_tag in tags:
            #     failed_course_by_tag = True

            failed = failed_course_by_tag or (total_failed_count >= 2)
            relation.positive_completion_possible = (not failed)
            relation.save()

        print("Processed all users for " + course.title)
