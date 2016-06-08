from django.contrib import admin
from PlagCheck.models import *
from django.core import urlresolvers

from AuroraProject.settings import PLAGCHECK as plagcheck_settings

class PlagCheckModelAdmin(admin.ModelAdmin):
    pass

class ReferenceAdmin(PlagCheckModelAdmin):
    #list_display = ('hash', 'stored_doc_id', )
    list_display = ('hash',)


class ResultAdmin(PlagCheckModelAdmin):
    #list_display = ('stored_doc_id', 'hash_count')
    list_display = ('hash_count',)


class SuspectsAdmin(PlagCheckModelAdmin):
    list_filter = ('state', )
    #list_display = ('id', 'link_to_stored_doc_id', 'link_to_similar_to_id', 'hash_count', 'match_count', 'similarity', 'state')
    list_display = ('id', 'hash_count', 'match_count', 'similarity', 'state')
    raw_id_fields = ('stored_doc', 'similar_to',)

    def link_to_stored_doc_id(self, obj):
        link = urlresolvers.reverse("admin:PlagCheck_store_change", args=[obj.stored_doc.id])
        return u'<a href="%s">%s</a>' % (link, obj.stored_doc.id)
    link_to_stored_doc_id.allow_tags = True
    link_to_stored_doc_id.short_description = 'stored doc'

    def link_to_similar_to_id(self, obj):
        link = urlresolvers.reverse("admin:PlagCheck_store_change", args=[obj.similar_to.id])
        return u'<a href="%s">%s</a>' % (link, obj.similar_to.id)
    link_to_similar_to_id.allow_tags = True
    link_to_similar_to_id.short_description = 'similar to'

    def hash_count(self, obj):
        return obj.result.hash_count

class SuspectFilterAdmin(PlagCheckModelAdmin):
    #list_display = ('id', 'stored_doc_id')
    list_display = ('id',)

class StoreAdmin(PlagCheckModelAdmin):
    list_display = ('id', 'elaboration_id')


admin.site.register(Store, StoreAdmin)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Suspect, SuspectsAdmin)
admin.site.register(SuspectFilter, SuspectFilterAdmin)
