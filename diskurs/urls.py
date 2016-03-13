from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<thread_id>[0-9]+)/newpost/$', views.new_post, name='new_post'),
    url(r'^(?P<thread_id>[0-9]+)/upvote/(?P<post_id>[0-9]+)/$', views.upvote_post, name='upvote_post'),
    url(r'^(?P<thread_id>[0-9]+)/downvote/(?P<post_id>[0-9]+)/$', views.downvote_post, name='downvote_post'),
    url(r'^(?P<thread_id>[0-9]+)/delete/(?P<post_id>[0-9]+)/$', views.delete_post, name='delete_post'),
    url(r'^(?P<thread_id>[0-9]+)/choose-group/$', views.choose_group, name='choose_group'),
    url(r'^(?P<thread_id>[0-9]+)/choose-group/set/(?P<group_id>[0-9]+)/$', views.choose_group_set,
        name='choose_group_set'),
    url(r'^(?P<thread_id>[0-9]+)/$', views.thread, name='thread'),
    url(r'^(?P<thread_id>[0-9]+)/post/(?P<post_id>[0-9]+)/$', views.thread_post, name='thread_post'),
    url(r'^(?P<thread_id>[0-9]+)/post/(?P<post_id>[0-9]+)/ajax/$', views.post_list, name='post_list'),
]
