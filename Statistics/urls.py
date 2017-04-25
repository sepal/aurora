from django.conf.urls import url

import Statistics.views

app_name = 'statistics'
urlpatterns = [
    url(r'^$', Statistics.views.statistics, name='home'),
]