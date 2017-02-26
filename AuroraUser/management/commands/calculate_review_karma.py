# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, UserManager
from AuroraUser.models import AuroraUser
from AuroraProject.settings import PROJECT_ROOT
from Course.models import CourseUserRelation
import datetime
import csv
import sys
import os

class Command(BaseCommand):
    help = 'Calculates the review carma for all users'

    def handle(self, *args, **options):
        calculate_review_karma()

def calculate_review_karma():
    for user in AuroraUser.objects.filter(is_staff=False, is_superuser=False):
        user.calculate_review_karma()

    log_karma_calculation()

def log_karma_calculation():
    log_file_path = os.path.dirname(PROJECT_ROOT) + '/AuroraUser/log/'
    log_file_name = 'karma_calculation_' + datetime.datetime.now().isoformat() + '.csv'
    field_names = [f.name for f in CourseUserRelation._meta.fields]

    log_file = open(log_file_path + log_file_name, 'w', newline='')
    writer = csv.writer(log_file)
    writer.writerow(['User ID', 'Course', 'Review Karma'])

    for instance in CourseUserRelation.objects.filter(user__is_staff=False, active=True).order_by('user_id', 'course_id'):
        writer.writerow([instance.user_id, instance.course.short_title, instance.review_karma])
