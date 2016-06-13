from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from datetime import datetime, date
# from Challenge.models import Challenge
import logging

class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    short_title = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    course_number = models.CharField(max_length=100, unique=True)
    start_date = models.DateField(default=datetime.now, blank=True)
    end_date = models.DateField(default=datetime.now, blank=True)

    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.title)

    def get_course_challenges(self):
        challenges = Challenge.models.Challenge.objects.filter(course=self)
        return list(challenges)

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
    user = models.ForeignKey('AuroraUser.AuroraUser')
    course = models.ForeignKey(Course)
    active = models.BooleanField(default=True)
    review_karma = models.DecimalField(max_digits=20, decimal_places=19, default=0.0)
    review_group = models.PositiveSmallIntegerField(default=1)
    top_reviewer = models.BooleanField(default=False)
