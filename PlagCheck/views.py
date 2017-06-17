from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse

from Elaboration.models import Elaboration
from PlagCheck.models import Suspicion, SuspicionState

from django.template import Template, Context


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
        context.update(options)

    request.session['selection'] = 'plagcheck_suspicions'
    request.session['count'] = count

    return {
        'html': render_to_string('plagcheck_suspicions.html', context, RequestContext(request)),
        'count': count,
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
