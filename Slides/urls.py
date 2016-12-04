from django.conf.urls import url

from .views import(slides)

urlpatterns = [
    url(r'^$', slides, name='slides'),
]