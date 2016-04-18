# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, UserManager
from AuroraUser.models import AuroraUser
from Course.models import *
from Challenge.models import Challenge
from Elaboration.models import Elaboration

class Command(BaseCommand):
    help = 'Deletes all course_user relations for users without an Elaboration'

    def handle(self, *args, **options):
        delete_users_without_first_elaboration()


def delete_users_without_first_elaboration():
    # Users who have not submitted an elaboration for this
    # challenges will be removed from the corresponding course
    challenge_list = [7,12]

    for challenge in Challenge.objects.filter(id__in=challenge_list):
        # Get the course for this challenge
        course = challenge.course
        for user in AuroraUser.objects.all():
            # Ignore staff and superusers
            if user.is_staff == True or user.is_superuser == True:
                continue
            # Get submitted elaborations for this user and challenge
            elaborations = Elaboration.objects.filter(challenge=challenge, user=user, submission_time__isnull=False)
            if len(elaborations) > 0:
                # User has submitted an elaboation for this challenge, dont't delete
                continue
            # User has not submitted an elaboration -> delete him from this course
            #CourseUserRelation.objects.filter(course=course, user=user).delete()
