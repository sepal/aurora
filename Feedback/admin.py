from django.contrib import admin
from .models import Lane
from suit.admin import SortableModelAdmin

@admin.register(Lane)
class LaneAdmin(SortableModelAdmin):
    fields = ('name', 'hidden')
    list_display = ('name', 'hidden', 'order')
    sortable = 'order'
