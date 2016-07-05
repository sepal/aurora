# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, UserManager
from AuroraUser.models import AuroraUser
from Course.models import *
from Challenge.models import *
from Elaboration.models import *


class Command(BaseCommand):
    help = 'Set positive completion flag'

    def handle(self, *args, **options):
        set_positive_completion_possible()


def set_positive_completion_possible():
    for course in Course.objects.all():
        for user in AuroraUser.objects.filter(is_staff=False, is_superuser=False):

            submitted_points = user.total_points_submitted(course)

            try:
                relation = CourseUserRelation.objects.get(
                    user=user, course=course)
                if submitted_points >= 57:
                    relation.positive_completion_possible = True
                else:
                    relation.positive_completion_possible = False

                relation.save()
            except:
                print("User " + user.nickname + " is not registerned in any courses, skipping.")

    # print(user.number_of_reviews_received(course))
    # print(user.number_of_reviews_rated(course))
    #
    # print(user.extra_points_earned_with_comments(course))
    # print(user.extra_points_earned_by_rating_reviews(course))
