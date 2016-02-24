from django.db import models
from Elaboration.models import Elaboration
from django.forms import model_to_dict
from django.db import connection
from django.db import transaction
from enum import IntEnum
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.utils.encoding import *


class Result(models.Model):
    """Just stores the result of a check of one document.
    """
    doc = models.ForeignKey(Elaboration)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    hash_count = models.IntegerField()

    def __unicode__(self):
        return self.id

    def celery_result(self):
        return model_to_dict(self)


class SuspectState(IntEnum):
    """SUSPECTED: Default state of a possible plagiarism document
    PLAGIARISM: The suspected document is plagiarism
    FALSE_POSITIVE: No plagiarism at all, could be improved by algorithm
    FILTER: Use the suspected document to filter future documents
    AUTO_FILTERED: Automatically given state when suspect has been filtered out by
    previous filters.
    CITED: The suspected document contained a ordinary citation to the similar document
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
    in a plagiarism suspect because the similarity reached its threshold.
    """

    DEFAULT_STATE = SuspectState.SUSPECTED

    doc = models.ForeignKey(Elaboration, related_name='suspected_doc')
    similar_to = models.ForeignKey(Elaboration, related_name='suspected_similar_to')
    percent = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    result = models.ForeignKey(Result)
    state = models.CharField(max_length=2, default=DEFAULT_STATE.value, choices=SuspectState.choices())
    match_count = models.IntegerField()

    def __unicode__(self):
        return self.id

    def __str__(self):
        return "doc:%i similar_to:%i percent:%i state:%s" % (self.doc_id, self.similar_to_id, self.percent, SuspectState(self.state).name)

    @property
    def suspect_state(self):
        return SuspectState(int(self.state))

    @suspect_state.setter
    def suspect_state(self, value):
        self.state = SuspectState(int(value)).value

    def my_get_next_or_previous_by_FIELD(self, field, is_next, *args, **kwargs):
        """Workaround to call get_next_or_previous_by_FIELD by using complext lookup queries using
        Djangos Q Class. The only difference between this version and original version is that
        positional arguments are also passed to the filter function.

        \see: http://stackoverflow.com/questions/35602780/django-get-next-by-field-using-complex-q-lookups
        """
        if not self.pk:
            raise ValueError("get_next/get_previous cannot be used on unsaved objects.")
        op = 'gt' if is_next else 'lt'
        order = '' if is_next else '-'
        param = force_text(getattr(self, field.attname))
        q = Q(**{'%s__%s' % (field.name, op): param})
        q = q | Q(**{field.name: param, 'pk__%s' % op: self.pk})
        qs = self.__class__._default_manager.using(self._state.db).filter(*args, **kwargs).filter(q).order_by('%s%s' % (order, field.name), '%spk' % order)
        try:
            return qs[0]
        except IndexError:
            raise self.DoesNotExist("%s matching query does not exist." % self.__class__._meta.object_name)

    def get_prev_next(self, show_filtered=False):
        next_id = None
        try:
            if show_filtered:
                next_id = self.get_next_by_created().id
            else:
                next_id = self.my_get_next_or_previous_by_FIELD(Suspect._meta.get_field('created'), True, ~Q(state=SuspectState.AUTO_FILTERED.value)).id
        except ObjectDoesNotExist:
            pass

        prev_id = None
        try:
            if show_filtered:
                prev_id = self.get_previous_by_created().id
            else:
                prev_id = self.my_get_next_or_previous_by_FIELD(Suspect._meta.get_field('created'), False, ~Q(state=SuspectState.AUTO_FILTERED.value)).id
        except ObjectDoesNotExist:
            pass

        return (prev_id, next_id)


class SuspectFilter(models.Model):
    """Provides filtering against a whole document, usually a suspected document is added
    as a filter. For a suspected document to be filtered it needs to match a filtered document
    with a similarity greater then the similarity threshold.

    TODO: implement filtering based on hashes, so that common parts between two document can be filtered.
    this would be especially helpful when filtering reviews, where the questions stay the same for each
    review
    """
    doc = models.ForeignKey(Elaboration, unique=True)

    @staticmethod
    def update_filter(suspect):
        if suspect.state is SuspectState.FILTER.value:
            try:
                SuspectFilter.objects.create(doc_id=suspect.doc_id)
            except IntegrityError:
                pass
        else:
            try:
                SuspectFilter.objects.get(doc_id=suspect.doc_id).delete()
            except ObjectDoesNotExist:
                pass


class Reference(models.Model):
    hash = models.CharField(db_index=True, max_length=255)
    doc = models.ForeignKey(Elaboration)

    # TODO: this causes a integrity error when inserting hashes, why?
    # class Meta:
    #    unique_together = (("hash", "doc"),)

    def __unicode__(self):
        return self.hash

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
    def remove_references(doc_id):
        try:
            Reference.objects.filter(doc_id=doc_id).delete()
        except Reference.DoesNotExist:
            pass

    @staticmethod
    def store_references(doc_id, hash_list):
        with transaction.atomic():
            for h in hash_list:
                Reference.objects.create(hash=h, doc_id=doc_id)
