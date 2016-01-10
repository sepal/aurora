from django.conf.urls import patterns, url

from FileUpload import views

urlpatterns = [
    url(r'^fileupload$', views.file_upload),
    url(r'^fileupload/all$', views.all_files),
    url(r'^fileupload/remove$', views.file_remove),
]