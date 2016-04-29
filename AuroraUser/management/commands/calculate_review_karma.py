# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, UserManager
from AuroraUser.models import AuroraUser

class Command(BaseCommand):
    help = 'Calculates the review carma for all users'

    def handle(self, *args, **options):
        calculate_review_karma()

def calculate_review_karma():
    for user in AuroraUser.objects.filter(is_staff=False, is_superuser=False):
        user.calculate_review_karma()
