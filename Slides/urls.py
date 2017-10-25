from django.conf.urls import url

from .views import (slides, slide_topics, slide_stack, search, refresh_structure)


app_name = 'slides'
urlpatterns = [
    url(r'^$', slides, name='slides'),
    url(r'^search/$', search, name='search'),
    url(r'^refreshstructure/$', refresh_structure, name='refreshstructure'),
    url(r'^(?P<topic>[^/]+)/$', slide_topics, name='slidetopics'),
    url(r'^(?P<topic>[^/]+)/(?P<slug>[^/]+)/$', slide_stack, name='slidestack'),
]
