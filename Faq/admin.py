from django.contrib import admin
from django.forms import ModelForm, TextInput

from Faq.models import Faq

from suit.admin import SortableModelAdmin
from suit.widgets import AutosizedTextarea


class FaqForm(ModelForm):
    class Meta:
        widgets = {
            'question': AutosizedTextarea(attrs={'class': 'input-xlarge'}),
            'answer': AutosizedTextarea(attrs={'class': 'input-xlarge'}),
        }


class FaqAdmin(SortableModelAdmin):
    form = FaqForm

    fieldsets = [
        (
            None, {
                'fields': [
                    'course',
                    'question',
                    'answer'
                ]
            }
        ),
    ]
    list_display = (
        'question',
        'answer',
    )
    sortable = 'order'

admin.site.register(Faq, FaqAdmin)
