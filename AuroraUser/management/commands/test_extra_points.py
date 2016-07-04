# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, UserManager
from AuroraUser.models import AuroraUser
from AuroraProject.settings import PROJECT_ROOT
from Course.models import *
from Challenge.models import *
from Elaboration.models import *
from Comments.models import *


class Command(BaseCommand):
    help = 'Test script for user extra points'

    def handle(self, *args, **options):
        test_extra_points()


def test_extra_points():
    user = AuroraUser.objects.get(id=319)
    course = Course.objects.get(id=1)

    print(user.number_of_reviews_received(course))
    print(user.number_of_reviews_rated(course))

    print(user.extra_points_earned_with_comments(course))
    print(user.extra_points_earned_by_rating_reviews(course))
