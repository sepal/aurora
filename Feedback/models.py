import datetime
import json
from django.db import models
from django.contrib import admin
from AuroraUser.models import AuroraUser
from Course.models import Course
from Comments.models import Comment


class Lane(models.Model):
    """
    A lane represents one column in the kanban.
    """

    name = models.CharField(max_length=100, unique=True)
    hidden = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

    def _is_last(self):
        return self.pk == Lane.objects.all().order_by('-order').first().pk

    archiving = property(_is_last)


class Issue(models.Model):
    """
    Issue is the content model for the feedback system.
    """

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

    def _get_serializable_teaser(self, is_staff=False):
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
            'upvotes': Upvote.objects.filter(issue=self).count(),
            'comments': self._number_of_comments(is_staff)
        }

        return data

    def get_serializable(self, is_staff=True):
        """
        Get the full issue information with all references as a dict which can
        be serialized into json or anything else.
        """
        data = self._get_serializable_teaser(is_staff)

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
            'body': self.body
        })
        return data

    def upvoted(self, user):
        """
        Returns True if the given user has upvoted this issue.
        """
        return Upvote.exists(user, self.pk)

    def _number_of_comments(self, is_staff=False):
        """ Callback for the number of comments property. """
        return  Comment.count_for('issue', self.pk, is_staff)

    number_of_comments = property(_number_of_comments)


class Upvote(models.Model):
    """
    Model which saves who up voted which issue.
    """

    user = models.ForeignKey(AuroraUser)
    issue = models.ForeignKey(Issue)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{0} upvoted {1}".format(self.user.nickname, self.issue.title)

    def __unicode__(self):
        return self.__str__()

    @staticmethod
    def exists(user, issue):
        """
        Checks if the given user has already upvoted the given issue.
        """
        return Upvote.objects.filter(user=user, issue=issue).count() > 0