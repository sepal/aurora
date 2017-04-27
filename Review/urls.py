from django.conf.urls import patterns, url

import Review.views

urlpatterns = [
    url(r'^$', Review.views.review, name='review'),
    url(r'^extra_review$', Review.views.extra_review, name='extra_review'),
    url(r'^review_answer$', Review.views.review_answer, name='review_answer'),
    url(r'^evaluate$', Review.views.evaluate, name='evaluate'),
]
