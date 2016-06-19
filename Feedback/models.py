from django.db import models
from django.contrib import admin
from AuroraUser.models import AuroraUser
from Course.models import Course

class Lane(models.Model):
    """Lane is a model one column in the feedback kanban."""
    name = models.CharField(max_length=100, unique=True)
    hidden = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

class Issue(models.Model):
    """Issue is the content model for the feedback system."""
    course = models.ForeignKey(Course)
    author = models.ForeignKey(AuroraUser)
    lane = models.ForeignKey(Lane)
    post_date = models.DateField()
    title = models.CharField(max_length=100)
    body = models.TextField()
