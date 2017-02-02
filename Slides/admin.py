from django.contrib import admin

# Register your models here.
from .models import Slide, SlideStack
from .structures import GsiDataStructure, HciDataStructure


admin.site.register(SlideStack)
admin.site.register(Slide)
