from django.conf.urls import url
import Notification.views
import Notification.feed

urlpatterns = [
   url(r'^write$', Notification.views.write_notification, name='write'),
   url(r'^send$', Notification.views.send_notification, name='send'),
   url(r'^read$', Notification.views.read, name='read'),
   url(r'^refresh$', Notification.views.refresh, name='refresh'),
   url(r'^$', Notification.views.notifications, name='list'),
   url(r'^feed/(?P<token>[^/]+)/$', Notification.feed.NotificationFeed(), name='feed'),
]

