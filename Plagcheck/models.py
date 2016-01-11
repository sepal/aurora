from django.db import models
from Elaboration.models import Elaboration
from django.forms import model_to_dict
from django.db import connection
from django.db import transaction


class Result(models.Model):
    overall_percentage = models.IntegerField()
    doc = models.ForeignKey(Elaboration)
    doc_version = models.IntegerField()
    doc_type = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    hash_count = models.IntegerField()

    def celery_result(self):
        return model_to_dict(self)


class Reference(models.Model):
    hash = models.CharField(db_index=True, max_length=255)
    doc = models.ForeignKey(Elaboration)

    @staticmethod
    def get_matching_count(doc_id):
        cursor = connection.cursor()

        # with inner join
        cursor.execute('SELECT * '
                       'FROM ('
                           'SELECT id as src_id, hash as src_hash, doc_id as src_doc_id '
                           'FROM Plagcheck_reference '
                           'WHERE doc_id = %s) as new '
                       'INNER JOIN Plagcheck_reference '
                       'ON new.src_hash=hash '
                       'WHERE doc_id != %s', [doc_id, doc_id])

        #SELECT * FROM (SELECT id as src_id, hash as src_hash, doc_id as src_doc_id FROM Plagcheck_reference WHERE doc_id = 32) as new INNER JOIN Plagcheck_reference WHERE new.src_hash=hash

        return cursor.rowcount

        # access references
        # for _row in cursor.fetchall():
        #    row = (id=_row[0],hash=_row[1],doc=_row[2])

    @staticmethod
    def del_ref(doc_id):
        try:
            Reference.objects.filter(doc_id=doc_id).delete()
        except Reference.DoesNotExist:
            pass

    @staticmethod
    def store(hash_list, doc_id):
        with transaction.atomic():
            for _hash in hash_list:
                hash_data = str(_hash)
                Reference.objects.create(hash=hash_data, doc_id=doc_id)
