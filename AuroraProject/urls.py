from . import views, settings

from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls.static import static

admin.autodiscover()


urlpatterns = [
    # TODO: add home without course
    url(r'^$', views.course_selection, name='course_selection'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),

    url(r'^comment/', include('Comments.urls', namespace='Comments')),
    url(r'^comments/', include('django_comments_xtd.urls')),

    url(r'result_users', views.result_users, name='result_users'),
    url(r'result_elabs_nonfinal', views.result_elabs_nonfinal, name='result_elabs_nonfinal'),
    url(r'result_elabs_final', views.result_elabs_final, name='result_elabs_final'),
    url(r'result_reviews', views.result_reviews, name='result_reviews'),

    url(r'^add_tags/$', views.add_tags),
    url(r'^remove_tag/$', views.remove_tag),
    url(r'^autocomplete_tag/$', views.autocomplete_tag),

    url(r'^/course/(?P<course_short_title>(\w+))/', include([
        url(r'^$', views.home, name='home'),
        url(r'^challenge/', include('Challenge.urls', namespace='Challenge')),
        url(r'^elaboration/', include('Elaboration.urls', namespace='Elaboration')),
        url(r'^review/', include('Review.urls', namespace='Review')),
        url(r'^notifications/', include('Notification.urls', namespace='Notification')),
        url(r'^evaluation/', include('Evaluation.urls', namespace='Evaluation')),
        url(r'^statistics/', include('Statistics.urls', namespace='Statistics')),
        url(r'^slides/', include('Slides.urls', namespace='Slides')),
        url(r'', include('AuroraUser.urls', namespace='User')),
        url(r'^diskurs/', include('diskurs.urls', namespace="diskurs")),
        url(r'^feedback/', include('Feedback.urls', namespace="Feedback")),
    ])),

    url(r'', include('FileUpload.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()