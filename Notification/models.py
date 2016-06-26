import os
import uuid

from django.core.urlresolvers import reverse
from django.db import models
from django.http.response import Http404

from AuroraProject.settings import STATIC_URL
from AuroraUser.models import AuroraUser


class Notification(models.Model):
    user = models.ForeignKey('AuroraUser.AuroraUser')
    course = models.ForeignKey('Course.Course')
    text = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100, default=os.path.join(STATIC_URL, 'img', 'info.jpg'))
    link = models.CharField(max_length=100, default="")
    creation_time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    BAD_REVIEW = "Unfortunately you received a bad review for challenge: "
    ENOUGH_PEER_REVIEWS = "You have received enough positive reviews to submit your final challenge: "
    SUBMISSION_EVALUATED = "Your submission was evaluated: "
    NEW_MESSAGE = "New message for your submission: "

    @staticmethod
    def bad_review(review):
        text = Notification.truncate_text(Notification.BAD_REVIEW + review.elaboration.challenge.title)
        course = review.elaboration.challenge.get_course()
        Notification(
            user=review.elaboration.user,
            course=course,
            text=text,
            image_url=review.elaboration.challenge.image.url,
            link=reverse('Challenge:challenge', kwargs={'course_short_title': course.short_title}) + "?id=" + str(
                review.elaboration.challenge.id)
        ).save()

    @staticmethod
    def enough_peer_reviews(review):
        user = review.elaboration.user
        final_challenge = review.elaboration.challenge.get_final_challenge()
        stack = final_challenge.get_stack()
        if stack.has_enough_peer_reviews(user) and not final_challenge.submitted_by_user(user):
            text = Notification.truncate_text(Notification.ENOUGH_PEER_REVIEWS + final_challenge.title)
            course = review.elaboration.challenge.get_course()
            Notification.objects.get_or_create(
                user=user,
                course=course,
                text=text,
                image_url=final_challenge.image.url,
                link=reverse('Challenge:stack', kwargs={'course_short_title': course.short_title}) + "?id=" + str(
                    review.elaboration.challenge.get_stack().id)
            )

    @staticmethod
    def truncate_text(text):
        if len(text) >= 100:
            text = text[0:96]
            text += "..."
        return text


class FeedToken(models.Model):
    user = models.ForeignKey('AuroraUser.AuroraUser')
    token = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    @staticmethod
    def create_new_token(user):
        FeedToken.objects.filter(user=user).delete()

        return FeedToken.objects.create(user=user)

    @staticmethod
    def get_user_by_token_or_raise_404(token):
        try:
            feed_token = FeedToken.objects.get(token=token)
            return AuroraUser.objects.get(pk=feed_token.user_id)
        except (AuroraUser.DoesNotExist, FeedToken.DoesNotExist):
            raise Http404
