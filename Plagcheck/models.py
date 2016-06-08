from django.db import models
from Elaboration.models import Elaboration
from django.forms import model_to_dict
from django.db import connection
from django.db import transaction
from enum import IntEnum

class Result(models.Model):
    similarity = models.IntegerField()
    doc = models.ForeignKey(Elaboration)
    doc_version = models.IntegerField()
    doc_type = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    hash_count = models.IntegerField()
    match_count = models.IntegerField()

    def __unicode__(self):
        return self.id

    def celery_result(self):
        return model_to_dict(self)


class Suspect(models.Model):
    doc = models.ForeignKey(Elaboration, related_name='suspected_doc')
    similar_to = models.ForeignKey(Elaboration, related_name='suspected_similar_to')
    percent = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    result = models.ForeignKey(Result)

    def __unicode__(self):
        return self.id

class Reference(models.Model):
    hash = models.CharField(db_index=True, max_length=255)
    doc = models.ForeignKey(Elaboration)

    def __unicode__(self):
        return self.hash

    @staticmethod
    def get_match_count(doc_id):
        cursor = connection.cursor()

        # with inner join
        cursor.execute('SELECT COUNT(DISTINCT hash) '
                       'FROM ('
                           'SELECT id as src_id, hash as src_hash, doc_id as src_doc_id '
                           'FROM Plagcheck_reference '
                           'WHERE doc_id = %s) as new '
                       'INNER JOIN Plagcheck_reference '
                       'ON new.src_hash=hash '
                       'WHERE doc_id != %s', [doc_id, doc_id])

        row = cursor.fetchone()

        return row[0]

    @staticmethod
    def get_similar_elaborations(doc_id):
        cursor = connection.cursor()

        # with inner join
        cursor.execute('SELECT doc_id, COUNT(doc_id) '
                       'FROM ('
                           'SELECT id as src_id, hash as src_hash, doc_id as src_doc_id '
                           'FROM Plagcheck_reference '
                           'WHERE doc_id = %s) as new '
                       'INNER JOIN Plagcheck_reference '
                       'ON new.src_hash=hash '
                       'WHERE doc_id != %s '
                       'GROUP BY doc_id', [doc_id, doc_id])

        ret = list()
        for row in cursor.fetchall():
            ret.append((row[0], row[1]))

        return ret

    @staticmethod
    def del_ref(doc_id):
        try:
            Reference.objects.filter(doc_id=doc_id).delete()
        except Reference.DoesNotExist:
            pass

    @staticmethod
    def store(hash_list, doc_id):
        with transaction.atomic():
            for hash in hash_list:
                Reference.objects.create(hash=hash, doc_id=doc_id)
