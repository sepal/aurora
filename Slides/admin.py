from django.contrib import admin
from Slides.models import Slide
from Slides.models import Lecture

class SlideAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'title',
                    'pub_date',
                    'filename',
                ]
            }
        ),
    ]
    list_display = ('title','pub_date','filename',)

admin.site.register(Slide, SlideAdmin)


class LectureAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'course',
                    'start',
                    'end',
                    'active',
                ]
            }
        ),
    ]
    list_display = ('course','start','end','active',)

admin.site.register(Lecture, LectureAdmin)