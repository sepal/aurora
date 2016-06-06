import json
from collections import OrderedDict
from enum import IntEnum

from django.forms import model_to_dict
from django.db import models
from django.db import connections
from django.db import transaction
from django.db import IntegrityError
from django.db.models import Lookup
from django.db.models.fields import Field
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import *

from AuroraProject.settings import PLAGCHECK as plagcheck_settings


@Field.register_lookup
class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


class Store(models.Model):
    doc_id = models.IntegerField(null=False)
    text = models.TextField(null=False)
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=100, null=True)
    submission_time = models.DateTimeField(null=True)
    is_revised = models.BooleanField(null=False, default=False)

    def get_user(self):
        return "DEPRECATED"
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
        info['Elaboration ID'] = self.doc_id
        info['Submission time'] = self.submission_time

        return info
    document_info = property(get_document_info)

class Result(models.Model):
    """Just stores the result of a check of one document.
    """

    stored_doc = models.ForeignKey(Store)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    hash_count = models.IntegerField()

    def __unicode__(self):
        return self.id

    def celery_result(self):
        return model_to_dict(self)


class SuspectState(IntEnum):
    """SUSPECTED: Default state of a possible plagiarism document.
    PLAGIARISM: The suspected document is plagiarism.
    FALSE_POSITIVE: No plagiarism at all, could be improved by algorithm
    FILTER: Use the suspected document to filter future documents. Which means filters
    cannot be applied to already checked documents.
    AUTO_FILTERED: Automatically given state when suspect has been filtered out by
    previous filters.
    CITED: The suspected document contained a ordinary citation to the similar document.
    """

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
    """Stores the result of a check against a individual document, resulting
    in a plagiarism suspect because the similarity reached its threshold value.

    If the suspected document hashes match with another suspected document hashes,
    whose state is set to FILTER, then the first document get the state AUTO_FILTERED.
    """

    DEFAULT_STATE = SuspectState.SUSPECTED

    stored_doc = models.ForeignKey(Store, related_name='suspected_doc')
    similar_to = models.ForeignKey(Store, related_name='suspected_similar_to')
    similarity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    result = models.ForeignKey(Result)
    state = models.CharField(max_length=2, default=DEFAULT_STATE.value, choices=SuspectState.choices())
    match_count = models.IntegerField()

    def __unicode__(self):
        return self.id

    def __str__(self):
        return "stored_doc:%i similar_to:%i percent:%i state:%s" % (self.stored_doc_id, self.similar_to_id, self.similarity, self.state_enum.name)

    @property
    def state_enum(self):
        """
        Provides a convenient method to read the state as an enum
        :exception ValueError - when the given state is invalid
        :return: The respective enum object for the state value
        """
        return SuspectState(int(self.state))

    @state_enum.setter
    def state_enum(self, value):
        """
        Provides a convenient method to set the state
        :exception ValueError - when the stored state is invalid
        :param value: int, string or enum representing the state
        """
        self.state = SuspectState(int(value)).value

    def get_prev_next(self, show_filtered=False):
        """
        Provides the ids to the next and previous Suspect object, depending
        on the show_filtered value.
        :param show_filtered: True if auto filtered Suspects should be taken into account.
        :return: Tuple (previous_id, next_id)
        """
        next_id = None
        try:
            if show_filtered:
                next_id = self.get_next_by_created().id
            else:
                next_id = self.get_next_by_created(state__ne=SuspectState.AUTO_FILTERED.value).id
        except ObjectDoesNotExist:
            pass

        prev_id = None
        try:
            if show_filtered:
                prev_id = self.get_previous_by_created().id
            else:
                prev_id = self.get_previous_by_created(state__ne=SuspectState.AUTO_FILTERED.value).id
        except ObjectDoesNotExist:
            pass

        return (prev_id, next_id)

    def get_suspect_info(self):
        info = OrderedDict()

        info['# hashes'] = self.result.hash_count
        info['# matching hashes'] = self.match_count
        info['Similarity'] = self.similarity
        info['Verification time'] = self.created

        return info

    suspect_info = property(get_suspect_info)


class SuspectFilter(models.Model):
    """Provides filtering against a whole document, usually a suspected document is added
    as a filter. For a suspected document to be filtered it needs to match a filtered document
    with a similarity greater then the similarity threshold.

    TODO: implement filtering based on hashes, so that only common parts between two document can be filtered.
    this would be especially helpful when filtering reviews, where the questions stay the same for each
    review.
    """
    stored_doc = models.ForeignKey(Store)

    @staticmethod
    def update_filter(suspect):
        if suspect.state is SuspectState.FILTER.value:
            try:
                SuspectFilter.objects.create(stored_doc_id=suspect.stored_doc_id)
            except IntegrityError:
                pass
        else:
            try:
                SuspectFilter.objects.get(stored_doc_id=suspect.stored_doc_id).delete()
            except ObjectDoesNotExist:
                pass


class Reference(models.Model):
    """
    Holds a hash and links it to the document where it is appearing.
    """
    hash = models.CharField(db_index=True, max_length=255)
    stored_doc = models.ForeignKey(Store)

    # TODO: this causes a integrity error when inserting hashes, why?
    # class Meta:
    #    unique_together = (("hash", "stored_doc"),)

    def __unicode__(self):
        return self.hash

    @staticmethod
    def remove_references(stored_doc_id):
        try:
            Reference.objects.filter(stored_doc_id=stored_doc_id).delete()
        except Reference.DoesNotExist:
            pass

    @staticmethod
    def store_references(stored_doc_id, hash_list):
        with transaction.atomic():
            for h in hash_list:
                Reference.objects.create(hash=h, stored_doc_id=stored_doc_id)

    @staticmethod
    def get_similar_elaborations(stored_doc_id):
        """
        Gives a list of similar elaborations in respect to stored_doc_id. The document
        with stored_doc_id has to be stored into the DB before calling this function.

        :param stored_doc_id: Document to check against.
        :return: List of Tuples (similar_doc_id, # similar hashes, filter id)
        """
        cursor = connections[plagcheck_settings['database']].cursor()

        # with inner join
        cursor.execute('SELECT "similar".stored_doc_id, COUNT("similar".stored_doc_id), "filter".id '
                       'FROM ('
                           'SELECT hash, stored_doc_id '
                           'FROM "PlagCheck_reference" '
                           'WHERE stored_doc_id = %s '
                           'GROUP BY hash, stored_doc_id'
                           ') as "suspect" '
                       'INNER JOIN "PlagCheck_reference" as "similar" ON "suspect".hash="similar".hash '
                       'LEFT OUTER JOIN "PlagCheck_suspectfilter" as "filter" ON "similar".stored_doc_id="filter".stored_doc_id '
                       'WHERE "similar".stored_doc_id != %s '
                       'GROUP BY "similar".stored_doc_id, "filter".id ', [stored_doc_id, stored_doc_id])

        ret = list()
        for row in cursor.fetchall():
            ret.append((row[0], row[1], row[2]))

        return ret


