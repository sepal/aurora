from django.db import models
from Elaboration.models import Elaboration
from django.forms import model_to_dict


class Result(models.Model):
    overall_p = models.IntegerField()
    doc = models.ForeignKey(Elaboration)
    doc_version = models.IntegerField()
    doc_type = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    hash_count = models.IntegerField()

    def celery_result(self):
        return model_to_dict(self)


class Reference(models.Model):
    hash = models.CharField(max_length=255)
    doc = models.ForeignKey(Elaboration)

