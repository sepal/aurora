from django.contrib import admin

from .models import Topic, Slide, Chapter


admin.site.register(Topic)
admin.site.register(Chapter)
admin.site.register(Slide)