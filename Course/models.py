from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from datetime import datetime, date
from Stack.models import *
import logging


class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    short_title = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    course_number = models.CharField(max_length=100, unique=True)
    start_date = models.DateField(default=datetime.now, blank=True)
    end_date = models.DateField(default=datetime.now, blank=True)
    tuwel_course_id = models.PositiveIntegerField(null=False)
    tuwel_course_stream_id = models.PositiveIntegerField(null=False)
    email = models.EmailField(null=False)

    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.title)

    def get_course_challenges(self):
        challenges = Challenge.models.Challenge.objects.filter(course=self)
        return list(challenges)

    def get_course_chapter_ids(self):
        return Stack.objects.filter(course=self).distinct('chapter_id').values_list('chapter_id', flat=True)

    def user_is_enlisted(self, user):
        try:
            CourseUserRelation.objects.get(user=user, course=self)
            return True
        except CourseUserRelation.DoesNotExist:
            return False

    def user_is_enlisted_and_active(self, user):
        try:
            CourseUserRelation.objects.get(user=user, course=self, active=True)
            return True
        except CourseUserRelation.DoesNotExist:
            return False

    def currently_active(self):
        today = date.today()
        if(today >= self.start_date and today <= self.end_date):
            return True
        return False

    @staticmethod
    def get_or_raise_404(short_title):
        try:
            return Course.objects.get(short_title=short_title)
        except ObjectDoesNotExist:
            raise Http404


class CourseUserRelation(models.Model):
    user = models.ForeignKey('AuroraUser.AuroraUser', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    review_karma_tutors = models.DecimalField(max_digits=20, decimal_places=19, default=0.0)
    review_karma_students = models.DecimalField(max_digits=20, decimal_places=19, default=0.0)
    top_reviewer = models.BooleanField(default=False)
    positive_completion_possible = models.BooleanField(default=True)
