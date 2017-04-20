from django.conf.urls import url

import Statistics.views

urlpatterns = [
    url(r'^$', Statistics.views.statistics, name='home'),
]