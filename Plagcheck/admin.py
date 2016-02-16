from django.contrib import admin
from Plagcheck.models import *
from django.core import urlresolvers


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('hash', 'doc', )


class ResultAdmin(admin.ModelAdmin):
    list_display = ('doc', 'doc_version', 'similarity', 'hash_count', 'match_count')


class SuspectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'doc', 'similar_to', 'percent', 'created', )

admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Suspect, SuspectsAdmin)
