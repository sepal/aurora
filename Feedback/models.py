from django.db import models
from django.contrib import admin

class Lane(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hidden = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
