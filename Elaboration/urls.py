from django.conf.urls import url
import Elaboration.views


app_name = 'elaboration'
urlpatterns = [
    url(r'^save$', Elaboration.views.save_elaboration, name='save'),
    url(r'^save_revision$', Elaboration.views.save_revision, name='save_revision'),
    url(r'^submit$', Elaboration.views.submit_elaboration, name='submit'),
]
