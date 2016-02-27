from django.contrib import admin
from PlagCheck.models import *
from django.core import urlresolvers


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('hash', 'doc', )


class ResultAdmin(admin.ModelAdmin):
    list_display = ('doc', 'hash_count')


class SuspectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'doc', 'similar_to', 'similarity', 'state')


class SuspectFilterAdmin(admin.ModelAdmin):
    list_display = ('id', 'doc')

admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Suspect, SuspectsAdmin)
admin.site.register(SuspectFilter, SuspectFilterAdmin)
