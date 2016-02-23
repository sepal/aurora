from django.db import models
from Elaboration.models import Elaboration
from django.forms import model_to_dict
from django.db import connection
from django.db import transaction
from enum import IntEnum


class Result(models.Model):
    #similarity = models.IntegerField()
    doc = models.ForeignKey(Elaboration)
    #doc_version = models.IntegerField()
    #doc_type = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    hash_count = models.IntegerField()
    #match_count = models.IntegerField()

    def __unicode__(self):
        return self.id

    def celery_result(self):
        return model_to_dict(self)


class SuspectState(IntEnum):
    SUSPECTED = 0
    PLAGIARISM = 1
    FALSE_POSITIVE = 2
    FILTER = 3
    AUTO_FILTERED = 4
    CITED = 5

    @staticmethod
    def states():
        states = []
        for state in SuspectState:
            states.append({'value': state.value, 'name': state.name})
        return states

    @staticmethod
    def choices():
        choices = []
        for state in SuspectState:
            choices.append((state.value, state.name))
        return choices


class Suspect(models.Model):
    doc = models.ForeignKey(Elaboration, related_name='suspected_doc')
    similar_to = models.ForeignKey(Elaboration, related_name='suspected_similar_to')
    percent = models.IntegerField()
    #created = models.DateTimeField(auto_now_add=True)
    result = models.ForeignKey(Result)
    state = models.IntegerField(default=SuspectState.SUSPECTED, choices=SuspectState.choices())
    match_count = models.IntegerField()

    def __unicode__(self):
        return self.id

    def __str__(self):
        return "doc:%i similar_to:%i percent:%i state:%s" % (self.doc_id, self.similar_to_id, self.percent, SuspectState(self.state).name)


class SuspectFilter(models.Model):
    doc = models.ForeignKey(Elaboration, unique=True)


class Reference(models.Model):
    hash = models.CharField(db_index=True, max_length=255)
    doc = models.ForeignKey(Elaboration)

    #class Meta:
    #    unique_together = (("hash", "doc"),)

    def __unicode__(self):
        return self.hash

    @staticmethod
    @DeprecationWarning
    def get_match_count(doc_id):
        cursor = connection.cursor()

        # with inner join
        cursor.execute('SELECT COUNT(DISTINCT ref.hash) '
                       'FROM ('
                           'SELECT id, hash, doc_id '
                           'FROM Plagcheck_reference '
                           'WHERE doc_id = %s '
                           'GROUP BY hash, doc_id'
                           ') as new '
                       'INNER JOIN Plagcheck_reference as ref ON new.hash=ref.hash '
                       'LEFT OUTER JOIN Plagcheck_suspectfilter as filter ON new.id=filter.doc_id'
                       'WHERE ref.doc_id != %s', [doc_id, doc_id])

        row = cursor.fetchone()

        return row[0]

    @staticmethod
    def get_similar_elaborations(doc_id):
        cursor = connection.cursor()

        # with inner join
        cursor.execute('SELECT similar.doc_id, COUNT(similar.hash), filter.id '
                       'FROM ('
                           'SELECT id, hash, doc_id '
                           'FROM Plagcheck_reference '
                           'WHERE doc_id = %s '
                           'GROUP BY hash, doc_id'
                           ') as suspect '
                       'INNER JOIN Plagcheck_reference as similar ON suspect.hash=similar.hash '
                       'LEFT OUTER JOIN Plagcheck_suspectfilter as filter ON similar.doc_id=filter.doc_id '
                       'WHERE similar.doc_id != %s '
                       'GROUP BY similar.doc_id', [doc_id, doc_id])

        ret = list()
        for row in cursor.fetchall():
            ret.append((row[0], row[1], row[2]))

        return ret

    @staticmethod
    def del_ref(doc_id):
        try:
            Reference.objects.filter(doc_id=doc_id).delete()
        except Reference.DoesNotExist:
            pass

    @staticmethod
    def store_references(doc_id, hash_list):
        with transaction.atomic():
            for hash in hash_list:
                Reference.objects.create(hash=hash, doc_id=doc_id)

    @staticmethod
    def remove_references(doc_id):
        Reference.objects.filter(doc_id=doc_id).delete()

    @staticmethod
    def overall_similarity(doc_id, hash_count):
        sum = 0
        similarities = Reference.get_similar_elaborations(doc_id)
        for (doc_id, similar_hashes, filter_id) in similarities:
            sum += similar_hashes

        return (100.0/hash_count)*sum
