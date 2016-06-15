from django.contrib import admin
from .models import Thread
from .models import Post


class ThreadAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'course',
                    'title',
                    'first_post',
                    'user',
                    'members_in_group',
                ]
            }
        ),
    ]
    search_fields = ('user__username', 'title')
    list_display = ('id', 'course', 'title', 'user', 'created_at', )


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'content',
                    'parent_post',
                    'user',
                    'group',
                    'deleted',
                ]
            }
        ),
    ]
    search_fields = ('user__username', 'content')
    list_display = ('id', 'content', 'user', 'created_at', )


# Register your models here.
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)