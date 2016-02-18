from django.conf.urls import patterns, url

import Challenge.views

urlpatterns = patterns('',
                       url(r'^stack$', Challenge.views.stack, name='stack'),
                       url(r'^myreviews$', Challenge.views.my_review, name='myreviews'),
                       url(r'^challenge$', Challenge.views.challenge, name='challenge'),
                       url(r'^$', Challenge.views.challenges, name='home'),
                       )
