from django.conf.urls import patterns, url

import Statistics.views

urlpatterns = [
    url(r'^$', Statistics.views.statistics, name='home'),
]