import datetime
import json
from django.db import models
from django.contrib import admin
from AuroraUser.models import AuroraUser
from Course.models import Course

class Lane(models.Model):
    """Lane is a model one column in the feedback kanban."""
    name = models.CharField(max_length=100, unique=True)
    hidden = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

class Issue(models.Model):
    """Issue is the content model for the feedback system."""
    ISSUE_TYPE = (
        ('bug', 'Bug'),
        ('feature_request', 'Feature Request'),
        ('feedback', 'Feedback'),
        ('security', 'Security')
    )

    course = models.ForeignKey(Course)
    author = models.ForeignKey(AuroraUser)
    lane = models.ForeignKey(Lane)
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
    type = models.CharField(max_length=25, choices=ISSUE_TYPE)
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()

    def _get_serializable_teaser(self):
        """
        Get the basic issue information as a dict which can be serialized into
        json or anything else.
        """
        data = {
            'id': self.pk,
            'lane': {
                'id': self.lane.pk,
                'name': self.lane.name
            },
            'type': self.type,
            'title': self.title,
        }

        return data

    serializable_teaser = property(_get_serializable_teaser)

    def _get_serializable(self):
        """
        Get the full issue information with all references as a dict which can
        be serialized into json or anything else.
        """

        data = self._get_serializable_teaser()

        data.update({
            'course': {
                'id': self.course.pk,
                'name': self.course.title
            },
            'author': {
                'id': self.author.pk,
                'name': self.author.nickname
            },
            'post_date': self.post_date.isoformat('T'),
            'body': self.body,
        })
        return data

    serializable = property(_get_serializable)

