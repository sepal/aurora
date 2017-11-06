from django.contrib import admin
from Stack.models import *

class StackAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'title',
                    'description',
                    'course',
                    'chapter',
                    'start_date',
                    'end_date',
                    'final_date',
                ]
            }
        ),
    ]
    list_display = ('id', 'title', 'description', 'course', 'start_date', 'end_date', 'final_date', )

class ChapterAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'name',
                ]
            }
        ),
    ]
    list_display = ('name','id',)

admin.site.register(Stack, StackAdmin)
admin.site.register(Chapter, ChapterAdmin)
