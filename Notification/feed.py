import logging

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from Notification.models import Notification, FeedToken
from Course.models import Course

logger = logging.getLogger(__name__)


class NotificationFeed(Feed):
    title = "Aurora personal notification feed"
    description = "Updates about your personal notifications."

    def link(self, obj):
        return reverse('Notification:list', kwargs={'course_short_title': obj['course'].short_title})

    def get_object(self, request, *args, **kwargs):

        feed = {
            'user': FeedToken.get_user_by_token_or_raise_404(kwargs['token']),
            'course': Course.get_or_raise_404(kwargs['course_short_title'])
        }

        return feed

    def items(self, obj):
        return Notification.objects.filter(user=obj['user'], course=obj['course']).order_by('-creation_time')

    def item_title(self, item):
        return Notification.truncate_text(item.text)

    def item_description(self, item):
        return item.text

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.link