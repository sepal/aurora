from django.contrib import admin
from Course.models import Course
from Course.models import CourseUserRelation

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'title',
                    'short_title',
                    'description',
                    'course_number',
                    'start_date',
                    'end_date',
                ]
            }
        ),
    ]
    list_display = ('id', 'title', 'short_title', 'description', 'course_number', 'start_date', 'end_date', )

admin.site.register(Course, CourseAdmin)


class CourseUserRelationAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'user',
                    'course',
                ]
            }
        ),
    ]
    list_display = ('id', 'user', 'course', )

admin.site.register(CourseUserRelation, CourseUserRelationAdmin)
