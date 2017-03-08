from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from AuroraUser import views

admin.autodiscover()

urlpatterns = [
   # namespace comes from main urls.py
   url(r'^login/$', views.login, name='login'),
   url(r'^signin/$', views.signin, name='signin'),
   url(r'^signout/$', views.signout, name='signout'),
   #url(r'^course/$', views.course),
   url(r'^profile/$', views.profile, name='profile'),
   url(r'^profile/save/$', views.profile_save, name='save'),
   url(r'^sso_auth_callback$', views.sso_auth_callback),
   url(r'^create_feed_token/$', views.create_feed_token, name='create_feed_token'),
]
