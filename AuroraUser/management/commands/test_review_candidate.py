# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, UserManager
from AuroraUser.models import AuroraUser
from AuroraProject.settings import PROJECT_ROOT
from Course.models import *
from Challenge.models import *
from Elaboration.models import *
import datetime
import csv
import sys
import os


class Command(BaseCommand):
    help = 'Calculates the review carma for all users'

    def handle(self, *args, **options):
        test_review_candidate()


def test_review_candidate():
    found_lower   = 0
    found_similar = 0
    found_random  = 0
    test_cases = 0

    # user = AuroraUser.objects.get(id=172)
    # challenge = Challenge.objects.get(id=93)
    # print(user.review_group(challenge.course))
    #
    # elab = Elaboration.get_review_candidate(challenge, user)

    #
    # elab = Elaboration.get_lower_karma_review_candidate(challenge, user)
    # elab = Elaboration.get_similar_karma_review_candidate(challenge, user)
    # elab = Elaboration.get_random_review_candidate(challenge, user)
    #
    # candidate = elab['candidate']
    # print('Chosen by: ' + elab['chosen_by'])
    # print(candidate.id)
    # print(candidate.number_of_reviews())
    # print(candidate.is_submitted())


    for course in Course.objects.all():
        print('Checking Course: ' + course.short_title)
        print ('Missing reviews: ' + str(Elaboration.get_missing_reviews(course).count()))

        for elaboration in Elaboration.get_missing_reviews(course):
            test_cases += 2
            challenge = elaboration.challenge
            user = elaboration.user

            lower_review   = Elaboration.get_lower_karma_review_candidate(challenge, user)
            similar_review = Elaboration.get_similar_karma_review_candidate(challenge, user)

            if lower_review['chosen_by'] != 'random':
                found_lower += 1
            else:
                found_random += 1

            if similar_review['chosen_by'] != 'random':
                found_similar += 1
            else:
                found_random +=1

    print('Test cases: ' + str(test_cases))
    print('Found lower karma: ' + str(found_lower))
    print('Found similar karma: ' + str(found_similar))
    print('Fallback to random karma: ' + str(found_random))


    # challenge = Challenge.objects.all()[0]
    # user = AuroraUser.objects.get(nickname="patse")
    #
    # Elaboration.get_lower_karma_review_candidate(challenge, user)
    # Elaboration.get_similar_karma_review_candidate(challenge, user)
