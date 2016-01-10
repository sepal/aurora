from django.contrib import admin
from Plagcheck.models import *


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('hash', 'doc', )


class ResultAdmin(admin.ModelAdmin):
    list_display = ('doc', 'doc_version', 'overall_p', 'hash_count')

admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Result, ResultAdmin)
