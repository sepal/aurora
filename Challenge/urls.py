from django.conf.urls import url

import Challenge.views


app_name = 'challenge'
urlpatterns = [
    url(r'^stack$', Challenge.views.stack, name='stack'),
    url(r'^challenge$', Challenge.views.challenge, name='challenge'),
    url(r'^$', Challenge.views.challenges, name='home'),
    url(r'^myreviews$', Challenge.views.my_review, name='myreviews'),
]