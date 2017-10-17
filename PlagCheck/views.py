# All plagcheck related views are inside Evaluation app, just templates are used from this app directory

from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import Http404
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from Elaboration.models import Elaboration
from PlagCheck.models import Suspicion, SuspicionState, Result, Document

def render_to_string_suspicions_view(request, course, options=None):
    suspicion_list = Suspicion.suspicion_list_by_request(request, course)

    if options:
        suspect_elab_filter = options.pop('filter_by_suspect_elaboration')
        if suspect_elab_filter:
            suspicion_list = suspicion_list.filter(suspect_doc__elaboration_id=suspect_elab_filter)


    count = suspicion_list.count()

    context = {
        'course': course,
        'suspicions': suspicion_list,
        'suspicion_states': SuspicionState.choices(),
        'current_suspicion_state_filter': int(request.GET.get('state', -1)),
        'suspicions_count': count,
        'open_new_window': False,
        'enable_state_filter': True,
    }

    if options:
        context.update(options);


    request.session['selection'] = 'plagcheck_suspicions'
    request.session['count'] = count

    return {
        'html': render_to_string('plagcheck_suspicions.html', context, RequestContext(request)),
        'count': count,
    }

notification_templates_suspect = {
    SuspicionState.PLAGIARISM.value: "suspect plagiarism text",
    SuspicionState.SUSPECTED.value: "suspect suspected text",
    SuspicionState.CITED.value: "suspect cited text",
}

notification_templates_similar = {
    SuspicionState.PLAGIARISM.value: "similar plagiarism text",
    SuspicionState.SUSPECTED.value: "similar suspected text",
    SuspicionState.CITED.value: "similar cited text",
}

def render_to_string_compare_view(request, course, suspicion_id):
    suspicion = Suspicion.objects.get(pk=suspicion_id)

    (prev_suspicion_id, next_suspicion_id) = suspicion.get_prev_next(
        state=SuspicionState.SUSPECTED.value,
        #suspect_doc__submission_time__range=(course.start_date, course.end_date),
        suspect_doc__submission_time__gt=course.start_date,
    )

    # pass no elaboration if one of the documents is from an older database
    try:
        similar_elaboration = suspicion.similar_doc.elaboration
    except Elaboration.DoesNotExist:
        similar_elaboration = None
    try:
        suspect_elaboration = suspicion.suspect_doc.elaboration
    except Elaboration.DoesNotExist:
        suspect_elaboration = None

    context = {
        'course': course,
        'suspicion': suspicion,
        'suspicion_states': SuspicionState.states(),
        'suspicion_states_class': SuspicionState.__members__,
        'next_suspicion_id': next_suspicion_id,
        'prev_suspicion_id': prev_suspicion_id,
        'similar_elaboration': similar_elaboration,
        'suspect_elaboration': suspect_elaboration,
        'notification_templates_suspect': notification_templates_suspect,
        'notification_templates_similar': notification_templates_similar,
    }

    # number of suspicious documents
    suspicions_count = Suspicion.objects.filter(
        state=SuspicionState.SUSPECTED.value).count()

    return {
        'html': render_to_string('plagcheck_compare.html', context, RequestContext(request)),
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
