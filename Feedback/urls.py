from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^issue/add$', views.index, name="issue_add"),
    url(r'^issue/(?P<issue_id>[\d]+[/]?)$', views.issue_display,
        name="issue_diplay"),
    url(r'^comments/(?P<issue_id>[\d]+[/]?)$', views.issue_comments,
        name="comments_display"),
    url(r'^api/issue/(?P<issue_id>[\d]+[/]?)$', views.api_issue,
        name="issue_api"),
    url(r'^api/issue$', views.api_new_issue, name="new_issue_api"),
]
