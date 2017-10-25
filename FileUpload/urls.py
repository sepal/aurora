from django.conf.urls import url

from .views import (file_upload, all_files, original_files, revised_files, file_remove)

app_name = 'file_upload'
urlpatterns = [
    url(r'^fileupload$', file_upload, name='file_upload'),
    url(r'^fileupload/all$', all_files, name='all_files'),
    url(r'^fileupload/original$', original_files, name='original_files'),
    url(r'^fileupload/revised$', revised_files, name='revised_files'),
    url(r'^fileupload/remove$', file_remove, name='file_remove'),
]