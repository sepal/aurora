from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.template import Template, Context

from Elaboration.models import Elaboration
from PlagCheck.models import Suspicion, SuspicionState

import datetime


class Semester:

    year = 0
    winter_summer = ''

    def __init__(self, name):

        self.year = int(name[0:-1])

        if name[4].upper() == 'W':
            self.winter_summer = 'W'
        elif name[4].upper() == 'S':
            self.winter_summer = 'S'

    def start(self):
        if self.winter_summer == 'W':
            return datetime.date(self.year, 10, 1)
        elif self.winter_summer == 'S':
            return datetime.date(self.year, 3, 1)

        return None

    def end(self):
        if self.winter_summer == 'W':
            return datetime.date(self.year + 1, 2, 1)
        elif self.winter_summer == 'S':
            return datetime.date(self.year, 7, 1)

        return None

    def __str__(self):
        return "{}{}".format(self.year, self.winter_summer.upper())

    @staticmethod
    def get_last_semesters():
        now = datetime.datetime.now()

        semesters = []

        for y in range(now.year - 5, now.year + 1):
            semesters.append("{0}S".format(y))
            semesters.append("{0}W".format(y))

        return semesters


def suspicions_by_request(request, course, filter_by_suspect_elab=None):

    context = {}
    filter = {
        'suspect_doc__submission_time__gt': course.start_date,
    }

    if filter_by_suspect_elab:
        filter['suspect_doc__elaboration_id'] = filter_by_suspect_elab

    if 'state' in request.GET:
        try:
            state_filter = int(request.GET.get('state', ''))
            filter['state'] = state_filter
            context['current_suspicion_state_filter'] = state_filter
        except ValueError:
            pass

    if 'suspect_semester' in request.GET:
        try:
            semester_filter = Semester(request.GET.get('suspect_semester'))

            context['current_suspect_semester_filter'] = str(semester_filter)
            filter['suspect_doc__submission_time__gte'] = semester_filter.start()
            filter['suspect_doc__submission_time__lte'] = semester_filter.end()
        except ValueError:
            pass

    if 'similar_semester' in request.GET:
        try:
            semester_filter = Semester(request.GET.get('similar_semester'))

            context['current_similar_semester_filter'] = str(semester_filter)
            filter['similar_doc__submission_time__gte'] = semester_filter.start()
            filter['similar_doc__submission_time__lte'] = semester_filter.end()
        except ValueError:
            pass


    if 'current_suspect_user_name_filter' in request.GET:
        user_filter = request.GET.get('current_suspect_user_name_filter', '')
        filter['suspect_doc__user_name__icontains'] = user_filter
        context['current_suspect_user_name_filter'] = user_filter

    if 'current_similar_user_name_filter' in request.GET:
        user_filter = request.GET.get('current_similar_user_name_filter', '')
        filter['similar_doc__user_name__icontains'] = user_filter
        context['current_similar_user_name_filter'] = user_filter

    suspicion_list = Suspicion.objects.filter(**filter)

    context['suspicions'] = suspicion_list
    context['suspicions_count'] = suspicion_list.count()

    return context


def render_to_string_suspicions_view(request, course, options=None):

    filter_by_suspect_elab = None
    if options and 'filter_by_suspect_elaboration' in options:
        filter_by_suspect_elab = options.pop('filter_by_suspect_elaboration')

    context = suspicions_by_request(request, course, filter_by_suspect_elab=filter_by_suspect_elab)

    context.update({
        'course': course,
        'suspicion_states': SuspicionState.choices(),
        'last_semesters': Semester.get_last_semesters(),
        'open_new_window': False,
        'enable_filters': True,
    })

    if options:
        context.update(options)

    request.session['selection'] = 'plagcheck_suspicions'
    request.session['count'] = context['suspicions_count']

    return {
        'html': render_to_string('plagcheck_suspicions.html', context, request),
        'count': context['suspicions_count'],
    }

# BEWARE: Notification texts must not exceed 100 characters
notification_templates_suspect = {
    SuspicionState.PLAGIARISM.value: "Your elaboration from challange {{ elaboration.challenge.title }} "
    "has been marked as PLAGIARISM. You will be contacted.",
    SuspicionState.SUSPECTED.value: "Your elaboration from challange {{ elaboration.challenge.title }} "
    "has been marked as SUSPECTED and will be verified.",
}
notification_templates_similar = {
    SuspicionState.PLAGIARISM.value: "Your elaboration from challange {{ elaboration.challenge.title }} "
    "has been plagiarised by another user. You will be contacted.",
    SuspicionState.SUSPECTED.value: "Your elaboration from challange {{ elaboration.challenge.title }} "
    "has been suspected to be plagiarised by another user.",
}


def render_notification_strings(notification_templates, context):
    rendered = {}
    _context = Context(context)
    for key, value in notification_templates.items():
        rendered[key] = Template(value).render(_context)
    return rendered


def render_to_string_compare_view(request, course, suspicion_id):
    suspicion = Suspicion.objects.get(pk=suspicion_id)

    (prev_suspicion_id, next_suspicion_id) = suspicion.get_prev_next(
        state=SuspicionState.SUSPECTED.value,
        #suspect_doc__submission_time__range=(course.start_date, course.end_date),
        suspect_doc__submission_time__gt=course.start_date,
    )

    challenge_base_url = reverse('Challenge:challenge', kwargs={'course_short_title': course.short_title})

    # pass no elaboration if one of the documents is from an older database
    similar_challenge_link = None
    suspect_challenge_link = None
    try:
        similar_elaboration = suspicion.similar_doc.elaboration
        similar_challenge_link = challenge_base_url + "?id=" + str(similar_elaboration.challenge.id)
    except Elaboration.DoesNotExist:
        similar_elaboration = None
    try:
        suspect_elaboration = suspicion.suspect_doc.elaboration
        suspect_challenge_link = challenge_base_url + "?id=" + str(similar_elaboration.challenge.id)
    except Elaboration.DoesNotExist:
        suspect_elaboration = None

    suspect_context = {
        'user': suspect_elaboration.user,
        'suspicion': suspicion,
        'elaboration': suspect_elaboration,
    }

    similar_context = {
        'user': similar_elaboration.user,
        'suspicion': suspicion,
        'elaboration': similar_elaboration,
    }

    context = {
        'course': course,
        'suspicion': suspicion,
        'suspicion_states': SuspicionState.states(),
        'suspicion_states_class': SuspicionState.__members__,
        'next_suspicion_id': next_suspicion_id,
        'prev_suspicion_id': prev_suspicion_id,
        'similar_elaboration': similar_elaboration,
        'suspect_elaboration': suspect_elaboration,
        'notification_templates_suspect': render_notification_strings(notification_templates_suspect, suspect_context),
        'notification_templates_similar': render_notification_strings(notification_templates_similar, similar_context),
        'similar_challenge_link': similar_challenge_link,
        'suspect_challenge_link': suspect_challenge_link,
    }

    # number of suspicious documents
    suspicions_count = Suspicion.objects.filter(
        state=SuspicionState.SUSPECTED.value).count()

    return {
        'html': render_to_string('plagcheck_compare.html', context, request),
        'count': suspicions_count,
    }


@staff_member_required
def set_suspicion_state(request, suspicion_id, suspicion_state):

    suspicion = Suspicion.objects.get(pk=suspicion_id)

    suspicion.state_enum = suspicion_state

    suspicion.save()

    return JsonResponse({})


@staff_member_required
def get_suspicion_state(request, suspicion_id):

    suspicion = Suspicion.objects.get(pk=suspicion_id)

    return JsonResponse({'suspicion_state': suspicion.state_enum.value})