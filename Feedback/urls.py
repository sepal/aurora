from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^api/issue/(?P<issue_id>[\d]+[/]?)$', views.issue, name="index"),
]