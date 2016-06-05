from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^post_form', views.post_form, name="post_form"),
    url(r'^new$', views.new, name="new")
]