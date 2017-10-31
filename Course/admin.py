from django.contrib import admin
from django.http import HttpResponse
from Course.models import Course
from Course.models import CourseUserRelation

def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=reviewkarma.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"user"),
        smart_str(u"course"),
    ])
    for obj in modeladmin.model.objects.all():
        writer.writerow([
            smart_str(obj.user),
            smart_str(obj.course),
            smart_str(obj.review_karma),
        ])
    return response
export_csv.short_description = u"Export CSV"


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
                    'active',
                    'review_karma_tutors',
                    'review_karma_students',
                    'top_reviewer',
                ]
            }
        ),
    ]
    list_display = ('id', 'user', 'course', 'active', )
    actions = [export_csv]

admin.site.register(CourseUserRelation, CourseUserRelationAdmin)
