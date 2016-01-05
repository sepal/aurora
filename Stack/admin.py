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
                    'start_date',
                    'end_date',
                ]
            }
        ),
    ]
    list_display = ('id', 'title', 'description', 'course', 'start_date', 'end_date', )

admin.site.register(Stack, StackAdmin)
