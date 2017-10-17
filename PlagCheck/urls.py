from django.conf.urls import patterns, url

import PlagCheck.views

urlpatterns = [
    url(r'^suspicion/(?P<suspicion_id>\d+)/$', PlagCheck.views.get_suspicion_state, name='get_suspicion_state'),
    url(r'^suspicion/(?P<suspicion_id>\d+)/(?P<suspicion_state>\d+)/$', PlagCheck.views.set_suspicion_state, name='set_suspicion_state'),
]