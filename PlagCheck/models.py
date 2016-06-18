import json
from collections import OrderedDict
from itertools import chain

from django.forms import model_to_dict
from django.db import models
from django.db import connections
from django.db import transaction
from django.db.models import Lookup
from django.db.models.fields import Field
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import *

from Elaboration.models import Elaboration

from PlagCheck.util.state import SuspicionState
from PlagCheck.util.settings import PlagCheckSettings


@Field.register_lookup
class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


class Document(models.Model):
    elaboration_id = models.IntegerField(null=False)
    text = models.TextField(null=False)
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=100, null=True)
    submission_time = models.DateTimeField(null=True)
    is_revised = models.BooleanField(null=False, default=False)

    def get_elaboration(self):
        return Elaboration.objects.get(pk=self.elaboration_id)
    elaboration = property(get_elaboration)

    def get_user(self):
        from AuroraUser.models import AuroraUser

        return AuroraUser.objects.get(pk=self.user_id)
    user = property(get_user)

    def get_clean_text(self):
        return self.text.lstrip('"').rstrip('"')
    clean_text = property(get_clean_text)

    def get_json_text(self):
        return json.dumps({'content': self.clean_text})
    json_text = property(get_json_text)

    def get_document_info(self):
        info = OrderedDict()

        info['Name'] = self.user_name
        info['User ID'] = self.user_id
        info['Elaboration ID'] = self.elaboration_id
        info['Submission time'] = self.submission_time

        return info
    document_info = property(get_document_info)

    def get_plagcheck_info(self):
        info = OrderedDict()

        info['# hashes'] = self.result_set.order_by('-created').all()[0].hash_count

        return info
    plagcheck_info = property(get_plagcheck_info)

    def was_submitted_during(self, course):

        submission_time = self.submission_time.date()

        #if submission_time > course.start_date\
        #        and submission_time < course.end_date:
        if submission_time >= course.start_date:
            return True
        return False

    @staticmethod
    def get_unverified_docs():
        docs = []

        outdated_verifications = Document.objects.raw(
            'SELECT "store".* '
            ' FROM "PlagCheck_result" as "result", "PlagCheck_document" as "store" '
            ' WHERE "result".doc_id = "store".id '
            '  AND "store".submission_time != "result".submission_time;'
        )

        missing_verifications = Document.objects.raw(
            'SELECT "store".* '
            ' FROM "PlagCheck_document" as "store" '
            ' LEFT OUTER JOIN "PlagCheck_result" as "result" '
            '  ON "store".id = "result".doc_id '
            '  WHERE "result".doc_id IS NULL;'
        )

        docs = sorted(
            chain(outdated_verifications, missing_verifications),
            key=lambda doc: doc.submission_time
        )

        return docs



class Result(models.Model):
    """Stores the result of a check of one document.
    """

    doc = models.ForeignKey(Document)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    hash_count = models.IntegerField()
    submission_time = models.DateTimeField(blank=False)

    def __unicode__(self):
        return self.id

    def celery_result(self):
        return model_to_dict(self)


class Suspicion(models.Model):
    """Stores the result of a check against a individual document, resulting
    in a plagiarism suspect because the similarity reached its threshold value.
    """

    DEFAULT_STATE = SuspicionState.SUSPECTED

    suspect_doc = models.ForeignKey(Document, related_name='suspicion_suspect')
    similar_doc = models.ForeignKey(Document, related_name='suspicion_similar')
    similarity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    result = models.ForeignKey(Result)
    state = models.CharField(max_length=2, default=DEFAULT_STATE.value, choices=SuspicionState.choices())
    match_count = models.IntegerField()

    def __unicode__(self):
        return self.id

    def __str__(self):
        return "suspect_doc:%i similar:%i percent:%i state:%s" % (self.suspect_doc_id, self.similar_doc_id, self.similarity, self.state_enum.name)

    class Meta:
        ordering = ['created']

    @property
    def state_enum(self):
        """
        Provides a convenient method to read the state as an enum
        :exception ValueError - when the given state is invalid
        :return: The respective enum object for the state value
        """
        return SuspicionState(int(self.state))

    @state_enum.setter
    def state_enum(self, value):
        """
        Provides a convenient method to set the state
        :exception ValueError - when the stored state is invalid
        :param value: int, string or enum representing the state
        """
        self.state = SuspicionState(int(value)).value

    def get_prev_next(self, **filter_args):
        """
        Provides the ids to the next and previous Suspect object.
        :return: Tuple (previous_id, next_id)
        """
        next_id = None
        try:
            next_id = self.get_next_by_created(**filter_args).id
        except ObjectDoesNotExist:
            pass

        prev_id = None
        try:
            prev_id = self.get_previous_by_created(**filter_args).id
        except ObjectDoesNotExist:
            pass

        return (prev_id, next_id)

    def get_suspicion_info(self):
        info = OrderedDict()

        info['# matching hashes'] = self.match_count
        info['Similarity'] = "{0} %".format(self.similarity)
        info['Verification date'] = self.created

        return info
    suspicion_info = property(get_suspicion_info)

    @staticmethod
    def get_suspected_elaborations(course):
        suspicions = Suspicion.objects.all()
        elaborations = []

        for suspicion in suspicions:
            elaboration = suspicion.suspect_doc.elaboration
            if elaboration.challenge.course == course:
                elaborations.append(elaboration)

        return elaborations


class Reference(models.Model):
    """
    Holds a hash and links it to the document where it is appearing.
    """
    hash = models.CharField(db_index=True, max_length=255)
    suspect_doc = models.ForeignKey(Document)

    # TODO: this causes a integrity error when inserting hashes, why?
    # class Meta:
    #    unique_together = (("hash", "suspect_doc"),)

    def __unicode__(self):
        return self.hash

    @staticmethod
    def remove_references(suspect_doc_id):
        try:
            Reference.objects.filter(suspect_doc_id=suspect_doc_id).delete()
        except Reference.DoesNotExist:
            pass

    @staticmethod
    def store_references(suspect_doc_id, hash_list):
        with transaction.atomic():
            for h in hash_list:
                Reference.objects.create(hash=h, suspect_doc_id=suspect_doc_id)

    @staticmethod
    def get_similar_elaborations(suspect_doc_id):
        """
        Gives a list of similar elaborations in respect to suspect_doc_id. The document
        with suspect_doc_id has to be stored into the DB before calling this function.

        :param suspect_doc_id: Document to check against.
        :return: List of Tuples (similar_doc_id, # similar hashes)
        """
        cursor = connections[PlagCheckSettings.database].cursor()

        # with inner join
        cursor.execute('SELECT "similar".suspect_doc_id, COUNT("similar".suspect_doc_id) '
                       'FROM ('
                           'SELECT hash, suspect_doc_id '
                           'FROM "PlagCheck_reference" '
                           'WHERE suspect_doc_id = %s '
                           'GROUP BY hash, suspect_doc_id'
                           ') as "suspicion" '
                       'INNER JOIN "PlagCheck_reference" as "similar" ON "suspicion".hash="similar".hash '
                       'WHERE "similar".suspect_doc_id != %s '
                       'GROUP BY "similar".suspect_doc_id ', [suspect_doc_id, suspect_doc_id])

        ret = list()
        for row in cursor.fetchall():
            ret.append((row[0], row[1]))

        return ret


