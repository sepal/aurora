from django.contrib import admin
from PlagCheck.models import *
from django.core import urlresolvers


class PlagCheckModelAdmin(admin.ModelAdmin):
    pass


class ReferenceAdmin(PlagCheckModelAdmin):
    #list_display = ('hash', 'suspect_doc_id', )
    list_display = ('hash',)


class ResultAdmin(PlagCheckModelAdmin):
    #list_display = ('doc_id', 'hash_count')
    list_display = ('hash_count',)


class SuspicionAdmin(PlagCheckModelAdmin):
    list_filter = ('state', )
    #list_display = ('id', 'link_to_suspect_doc_id', 'link_to_similar_doc_id', 'hash_count', 'match_count', 'similarity', 'state')
    list_display = ('id', 'hash_count', 'match_count', 'similarity', 'state')
    raw_id_fields = ('suspect_doc', 'similar_doc',)

    def link_to_suspect_doc_id(self, obj):
        link = urlresolvers.reverse("admin:PlagCheck_document_change", args=[obj.suspect_doc.id])
        return u'<a href="%s">%s</a>' % (link, obj.suspect_doc.id)
    link_to_suspect_doc_id.allow_tags = True
    link_to_suspect_doc_id.short_description = 'suspect doc'

    def link_to_similar_doc_id(self, obj):
        link = urlresolvers.reverse("admin:PlagCheck_document_change", args=[obj.similar_doc.id])
        return u'<a href="%s">%s</a>' % (link, obj.similar_doc.id)
    link_to_similar_doc_id.allow_tags = True
    link_to_similar_doc_id.short_description = 'similar to'

    def hash_count(self, obj):
        return obj.result.hash_count


class DocumentAdmin(PlagCheckModelAdmin):
    list_display = ('id', 'elaboration_id')


admin.site.register(Document, DocumentAdmin)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Suspicion, SuspicionAdmin)
