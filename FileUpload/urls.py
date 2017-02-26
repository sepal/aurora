from django.conf.urls import patterns, url


urlpatterns = [
    url(r'^fileupload$', 'FileUpload.views.file_upload'),
    url(r'^fileupload/all$', 'FileUpload.views.all_files'),
    url(r'^fileupload/original$', 'FileUpload.views.original_files'),
    url(r'^fileupload/revised$', 'FileUpload.views.revised_files'),
    url(r'^fileupload/remove$', 'FileUpload.views.file_remove'),
]