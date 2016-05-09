# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, UserManager
from AuroraUser.models import AuroraUser
from AuroraProject.settings import PROJECT_ROOT
from Course.models import CourseUserRelation
from Challenge.models import *
import datetime
import csv
import sys
import os


class Command(BaseCommand):
    help = 'Calculates the review carma for all users'

    def handle(self, *args, **options):
        test_review_candidate()


def test_review_candidate():
    challenge = Challenge.objects.all()[0]
    user = AuroraUser.objects.get(nickname="patse")

    Elaboration.get_lower_karma_review_candidate(challenge, user)
    Elaboration.get_similar_karma_review_candidate(challenge, user)
