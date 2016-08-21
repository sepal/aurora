from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^issue/(?P<issue_id>[\d]+[/]?)$', views.issue, name="issue_diplay"),
    url(r'^api/issue/(?P<issue_id>[\d]+[/]?)$', views.api_issue, name="issue_api"),
]