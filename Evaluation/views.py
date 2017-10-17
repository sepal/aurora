from datetime import datetime
import json
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from taggit.models import TaggedItem
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView

from AuroraProject.decorators import aurora_login_required
from AuroraProject.views import CourseMixin
from Challenge.models import Challenge
from Course.models import Course, CourseUserRelation
from Elaboration.models import Elaboration
from Evaluation.models import Evaluation
from AuroraUser.models import AuroraUser
from Review.models import Review, ReviewEvaluation
from ReviewAnswer.models import ReviewAnswer
from ReviewQuestion.models import ReviewQuestion
from Stack.models import Stack
from Notification.models import Notification
from PlagCheck.models import Suspicion, SuspicionState, Result, Document
from middleware.AuroraAuthenticationBackend import AuroraAuthenticationBackend
from functools import lru_cache


@aurora_login_required()
@staff_member_required
def evaluation(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)
    overview = ""
    elaborations = []
    count = 0
    selection = request.session.get('selection', 'error')

    if selection not in ('error', 'questions', 'plagcheck_suspicions'):
        for serialized_elaboration in serializers.deserialize('json', request.session.get('elaborations', {})):
            elaborations.append(serialized_elaboration.object)
        if selection == 'search':
            display_points = request.session.get('display_points', 'error')
            if display_points == "true":
                user = AuroraUser.objects.get(
                    username=request.session.get('selected_user'))
                points = get_points(request, user, course)
                data = {
                    'elaborations': elaborations,
                    'search': True,
                    'stacks': points['stacks'],
                    'courses': points['courses'],
                    'review_evaluation_data': points['review_evaluation_data'],
                    'course': course
                }
            else:
                data = {'elaborations': elaborations,
                        'search': True, 'course': course}
        elif selection == 'complaints':
            data = {'elaborations': elaborations,
                    'course': course, 'complaints': 'true'}
        else:
            data = {'elaborations': elaborations, 'course': course}

        data["selection"] = selection

        if selection == "final_evaluation_new":
            overview = render_to_string('overview_new.html', context=data, request=request)
        else:
            overview = render_to_string('overview.html', context=data, request=request)
        count = len(elaborations)
    elif selection == 'questions':
        # get selected challenges from session
        challenges = []
        for serialized_challenge in serializers.deserialize('json', request.session.get('challenges', {})):
            challenges.append(serialized_challenge.object)
        count = len(challenges)
        overview = render_to_string('questions.html', context={'challenges': challenges}, request=request)
    elif selection == 'plagcheck_suspicions':
        suspicion_list = Suspicion.objects.filter(
            state=SuspicionState.SUSPECTED.value,
            #suspect_doc__submission_time__range=(course.start_date, course.end_date),
            suspect_doc__submission_time__gt=course.start_date,
        )

        count = suspicion_list.count()

        context = {
            'course': course,
            'suspicions': suspicion_list,
            'suspicion_states': SuspicionState.choices(),
            'suspicions_count': count,
        }

        overview = render_to_string('plagcheck_suspicions.html', context=context, request=request)

    challenges = Challenge.objects.all()

    return render(request, 'evaluation.html',
                              {'challenges': challenges,
                               'overview': overview,
                               'count_' + selection: count,
                               'stabilosiert_' + selection: 'stabilosiert',
                               'course': course,
                               'selection': selection,
                               'selected_challenge': request.session.get('selected_challenge'),
                               'selected_user': request.session.get('selected_user'),
                               'selected_task': request.session.get('selected_task'),
                               })


class EvaluationView(CourseMixin, TemplateView):
    #template_name = "evaluation.html"
    #template_name = "evaluation_list_detail.html"
    mode_template_names = {
        "overview": "evaluation.html",
        "export": "evaluation_export.html",
    }
    overview_template_name = "overview.html"
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    @method_decorator(aurora_login_required())
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        self.mode = kwargs.get("mode")
        if self.mode is None:
            self.mode = "overview"
        self.elaborations = self._get_elaborations()
        self._update_session()

        return super().dispatch(*args, **kwargs)

    def get_template_names(self):
        return (self.mode_template_names[self.mode],)

    def _update_session(self):
        # store selected elaborations in session
        self.request.session['elaborations'] = serializers.serialize(
            'json', self.elaborations)
        self.request.session['selection'] = self.selection_name
        self.request.session['count'] = len(self.elaborations)
        self.request.session.update(self.get_extra_session())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "overview": render_to_string(self.overview_template_name,
                                    context=self.get_overview_context_data(),
                                    request=self.request),
            "count_" + self.selection_name: self.request.session.get('count', '0'),
            "stabilosiert_" + self.selection_name: 'stabilosiert',
            "selection": self.selection_name,
            "course": self.course,
            "elaborations": self.elaborations,
        })

        return context

    def get_extra_session(self):
        return {}

    def get_elaborations(self):
        raise NotImplemented

    def _get_elaborations(self):
        elaborations = self.get_elaborations()

        # sort elaborations by submission time
        if type(elaborations) == list:
            elaborations.sort(key=lambda elaboration: elaboration.submission_time)
        else:
            elaborations = elaborations.order_by('submission_time')

        return elaborations

    def get_overview_context_data(self):
        return {
            'elaborations': self.elaborations,
            'course': self.course,
            "selection": self.selection_name,
        }


class MissingReviewsView(EvaluationView):
    selection_name = "missing_reviews"
    def get_elaborations(self):
        return Elaboration.get_missing_reviews(self.course)

missing_reviews = MissingReviewsView.as_view()


class NonAdequateWorkView(EvaluationView):
    selection_name = "non_adequate_work"
    def get_elaborations(self):
        return Elaboration.get_non_adequate_work(self.course)

non_adequate_work = NonAdequateWorkView.as_view()


class TopLevelTasksView(EvaluationView):
    selection_name = "top_level_tasks"
    def get_elaborations(self):
        return Elaboration.get_top_level_tasks(self.course)

top_level_tasks = TopLevelTasksView.as_view()


class FinalEvaluationTopLevelTasksView(EvaluationView):
    selection_name = "final_evaluation_top_level_tasks"
    def get_elaborations(self):
        return Elaboration.get_final_evaluation_top_level_tasks(self.course)

final_evaluation_top_level_tasks = FinalEvaluationTopLevelTasksView.as_view()


class FinalEvaluationNewView(EvaluationView):
    selection_name = "final_evaluation_new"
    overview_template_name = "overview_new.html"
    def get_elaborations(self):
        return Elaboration.get_final_evaluation_top_level_tasks(self.course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        count = self.request.session.get('final_evaluation_count', '0')
        context["count_final_evaluation_new"] = count
        return context

final_evaluation_new = FinalEvaluationNewView.as_view()


class ComplaintsView(EvaluationView):
    selection_name = "complaints"
    def get_elaborations(self):
        return Elaboration.get_complaints(self.course)

    def get_overview_context_data(self):
        context = super().get_overview_context_data()
        context["complaints"] = "true"
        return context

complaints = ComplaintsView.as_view()


class AwesomeView(EvaluationView):
    selection_name = "awesome"
    def get_elaborations(self):
        selected_challenge = self.request.session.get('selected_challenge', 'task...')
        if selected_challenge != 'task...':
            selected_challenge = selected_challenge[
                :(selected_challenge.rindex('(') - 1)]
            challenge = Challenge.objects.get(
                title=selected_challenge, course=self.course)
            elaborations = Elaboration.get_awesome_challenge(self.course, challenge)
        else:
            elaborations = Elaboration.get_awesome(self.course)
        self.selected_challenge = selected_challenge
        return elaborations

    def get_extra_session(self):
        return {
            "selected_challenge": "task..."
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_challenge"] = self.selected_challenge
        return context

awesome = AwesomeView.as_view()


class QuestionsView(EvaluationView):
    selection_name = "questions"
    overview_template_name = "questions.html"
    def get_elaborations(self):
        self.challenges = Challenge.get_questions(self.course)
        return []

    def get_overview_context_data(self):
        context = super().get_overview_context_data()
        context["challenges"] = self.challenges
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["challenges"] = self.challenges
        return context

    def get_extra_session(self):
        return {
            "challenges": serializers.serialize('json', self.challenges),
            "count": len(self.challenges),
        }

questions = QuestionsView.as_view()


@aurora_login_required()
@staff_member_required
def overview(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)
    elaboration = Elaboration.objects.get(pk=request.GET.get('elaboration_id'))
    user = elaboration.user
    stack = elaboration.challenge.get_stack()
    stack_challenges = stack.get_challenges()

    next_elaboration = None
    try:
        # elaborations = Elaboration.get_final_evaluation_top_level_tasks(course) | Elaboration.objects.filter(id=elaboration.id)
        # all_elaborations = list(elaborations.order_by('submission_time'))

        elaborations = []
        for serialized_elaboration in serializers.deserialize('json', request.session.get('elaborations', {})):
            elaborations.append(serialized_elaboration.object)

        next_index = elaborations.index(elaboration) + 1
        if next_index < len(elaborations):
            next_elaboration = elaborations[next_index]
        else:
            next_elaboration = None
    except ValueError:
        next_elaboration = None

    challenges = []
    for challenge in stack_challenges:
        challenge_data = {}
        challenge_data['challenge'] = challenge
        challenge_data['final'] = challenge.is_final_challenge()

        elaboration =  challenge.get_elaboration(user)
        challenge_data['elaboration'] = elaboration
        challenge_data['reviews'] = challenge.get_reviews_written_by_user(user)
        challenge_data['reveiced_reviews'] = Review.objects.filter(elaboration=elaboration, submission_time__isnull=False)
        challenges.append(challenge_data)

    data = {}
    data['course'] = course
    data['elaboration_user'] = user
    data['stack'] = stack
    data['challenges'] = challenges
    data['elaboration'] = elaboration
    data['next_elaboration'] = next_elaboration

    evaluation = None
    lock = False

    if Evaluation.objects.filter(submission=elaboration):
        evaluation = Evaluation.objects.get(submission=elaboration)
        if evaluation.tutor != request.user and not evaluation.is_older_15min():
            lock = True

    data['evaluation'] = evaluation
    data['evaluation_locked'] = lock

    return render(request, 'evaluation_overview.html', data)


@aurora_login_required()
@staff_member_required
def detail(request, course_short_title=None):

    course = Course.get_or_raise_404(short_title=course_short_title)

    # get selected elaborations from session
    elaborations = []
    params = {}
    for serialized_elaboration in serializers.deserialize('json', request.session.get('elaborations', {})):
        elaborations.append(serialized_elaboration.object)
    selection = request.session.get('selection', 'error')

    if 'elaboration_id' not in request.GET:
        raise Http404

    try:
        elaboration_id = int(request.GET.get('elaboration_id', ''))
    except ValueError:
        raise Http404()

    elaboration = Elaboration.objects.get(pk=elaboration_id)
    # store selected elaboration_id in session
    request.session['elaboration_id'] = elaboration.id

    if selection == "missing_reviews":
        questions = ReviewQuestion.objects.filter(
            challenge=elaboration.challenge).order_by("order")
        params = {'questions': questions, 'selection': 'missing reviews'}
    if selection == "top_level_tasks" or selection == 'final_evaluation_top_level_tasks':
        evaluation = None
        user = request.user
        lock = False
        if Evaluation.objects.filter(submission=elaboration):
            evaluation = Evaluation.objects.get(submission=elaboration)
            if evaluation.tutor != user and not evaluation.is_older_15min():
                lock = True
        params = {'evaluation': evaluation,
                  'lock': lock, 'selection': 'top-level tasks'}
    if selection == "non_adequate_work":
        params = {'selection': 'non-adequate work'}
    if selection == "complaints":
        if elaboration.challenge.is_final_challenge():
            evaluation = None
            user = request.user
            lock = False
            if Evaluation.objects.filter(submission=elaboration):
                evaluation = Evaluation.objects.get(submission=elaboration)
                if evaluation.tutor != user and not evaluation.is_older_15min():
                    lock = True
            params = {'evaluation': evaluation,
                      'lock': lock, 'selection': 'complaints'}
        else:
            params = {'selection': 'complaints'}
    if selection == "awesome":
        params = {'selection': 'awesome'}
    if selection == "evaluated_non_adequate_work":
        params = {'selection': 'evaluated non-adequate work'}
    if selection == "search":
        evaluation = None
        user = request.user
        lock = False
        if Evaluation.objects.filter(submission=elaboration):
            evaluation = Evaluation.objects.get(submission=elaboration)
            if evaluation.tutor != user and not evaluation.is_older_15min():
                lock = True
        if elaboration.challenge.is_final_challenge():
            params = {'evaluation': evaluation,
                      'lock': lock, 'selection': 'top-level tasks'}
        else:
            if elaboration.is_reviewed_2times():
                params = {'evaluation': evaluation, 'lock': lock}
            else:
                questions = ReviewQuestion.objects.filter(
                    challenge=elaboration.challenge).order_by("order")
                params = {'questions': questions,
                          'selection': 'missing reviews'}

    reviews = Review.objects.filter(
        elaboration=elaboration, submission_time__isnull=False)

    next = prev = None

    try:
        index = elaborations.index(elaboration)
        if index + 1 < len(elaborations):
            next = elaborations[index + 1].id
        if not index == 0:
            prev = elaborations[index - 1].id
        count_next = len(elaborations) - index - 1
        count_prev = index
    except ValueError:
        index = 0
        count_next = 0
        count_prev = 0

    stack_elaborations = elaboration.user.get_stack_elaborations(
        elaboration.challenge.get_stack())
    # sort stack_elaborations by submission time
    if type(stack_elaborations) == list:
        stack_elaborations.sort(
            key=lambda stack_elaboration: stack_elaboration.submission_time)
    else:
        stack_elaborations = stack_elaborations.order_by('submission_time')

    params['elaboration'] = elaboration
    params['stack_elaborations'] = stack_elaborations
    params['reviews'] = reviews
    params['next'] = next
    params['prev'] = prev
    params['count_next'] = count_next
    params['count_prev'] = count_prev
    params['course'] = course

    detail_html = render_to_string('detail.html', context=params, request=request)

    challenges = Challenge.objects.all()
    return render(request, 'evaluation.html', {'challenges': challenges, 'course': course, 'detail_html': detail_html})


@aurora_login_required()
@staff_member_required
def start_evaluation(request, course_short_title=None):
    if not 'elaboration_id' in request.GET:
        return False

    elaboration = Elaboration.objects.get(
        pk=request.GET.get('elaboration_id', ''))

    # set evaluation lock
    state = 'open'
    user = request.user
    if Evaluation.objects.filter(submission=elaboration):
        evaluation = Evaluation.objects.get(submission=elaboration)
        if evaluation.tutor == user:
            evaluation.lock_time = datetime.now()
            evaluation.save()
        else:
            if evaluation.is_older_15min():
                evaluation.lock_time = datetime.now()
                evaluation.tutor = user
                evaluation.save()
            else:
                state = 'locked by ' + evaluation.tutor.username
    else:
        evaluation = Evaluation.objects.create(
            submission=elaboration, tutor=user)
        evaluation.lock_time = datetime.now()
        evaluation.save()
        state = 'init'

    return HttpResponse(state)


@aurora_login_required()
@staff_member_required
def stack(request, course_short_title=None):
    elaboration = Elaboration.objects.get(
        pk=request.session.get('elaboration_id', ''))
    stack_elaborations = elaboration.user.get_stack_elaborations(
        elaboration.challenge.get_stack())

    return render(request, 'tasks.html', {'stack_elaborations': stack_elaborations})


@aurora_login_required()
@staff_member_required
def others(request, course_short_title=None):
    # get selected elaborations from session
    elaboration = Elaboration.objects.get(
        pk=request.session.get('elaboration_id', ''))

    next = prev = None

    if elaboration.get_others():
        other_elaborations = elaboration.get_others()

        index = int(request.GET.get('page', '0'))
        elaboration_list = list(other_elaborations)

        if index + 1 < len(elaboration_list):
            next = index + 1
        if not index == 0:
            prev = index - 1

        elaboration = elaboration_list[index]
    else:
        elaboration = []

    evaluation = None
    if elaboration.challenge.is_final_challenge():
        if Evaluation.objects.filter(submission=elaboration, submission_time__isnull=False):
            evaluation = Evaluation.objects.get(
                submission=elaboration, submission_time__isnull=False)

    return render(request, 'others.html',
                              {'elaboration': elaboration, 'evaluation': evaluation, 'next': next, 'prev': prev})


@aurora_login_required()
@staff_member_required
def challenge_txt(request, course_short_title=None):
    elaboration = Elaboration.objects.get(
        pk=request.session.get('elaboration_id', ''))
    return render(request, 'challenge_txt.html',
                              {'challenge': elaboration.challenge,
                                  'stack': elaboration.challenge.get_stack()})


@aurora_login_required()
@staff_member_required
def user_detail(request, course_short_title=None):
    user = Elaboration.objects.get(
        pk=request.session.get('elaboration_id', '')).user
    display_points = request.session.get('display_points', 'error')
    return render(request, 'user.html', {'user': user, 'course_short_title': course_short_title})


@csrf_exempt
@staff_member_required
def save_evaluation(request, course_short_title=None):
    elaboration_id = request.POST['elaboration_id']
    evaluation_text = request.POST['evaluation_text']
    evaluation_points = request.POST['evaluation_points']

    elaboration = Elaboration.objects.get(pk=elaboration_id)
    evaluation = Evaluation.objects.get(submission=elaboration)

    if evaluation_text:
        evaluation.evaluation_text = evaluation_text
    if evaluation_points:
        evaluation.evaluation_points = evaluation_points
    evaluation.save()

    return HttpResponse()


@csrf_exempt
@staff_member_required
def submit_evaluation(request, course_short_title=None):
    elaboration_id = request.POST['elaboration_id']
    evaluation_text = request.POST['evaluation_text']
    evaluation_points = request.POST['evaluation_points']

    elaboration = Elaboration.objects.get(pk=elaboration_id)
    user = request.user
    course = elaboration.challenge.course

    if Evaluation.objects.filter(submission=elaboration):
        evaluation = Evaluation.objects.get(submission=elaboration)
    else:
        evaluation = Evaluation.objects.create(submission=elaboration)

    evaluation.user = user = user
    evaluation.evaluation_text = evaluation_text
    evaluation.evaluation_points = evaluation_points
    evaluation.submission_time = datetime.now()
    evaluation.save()
    obj, created = Notification.objects.get_or_create(
        user=elaboration.user,
        course=course,
        text=Notification.SUBMISSION_EVALUATED + elaboration.challenge.title,
        image_url=elaboration.challenge.image.url,
        link=reverse('Challenge:stack', args=[
                     course_short_title]) + '?id=' + str(elaboration.challenge.get_stack().id)
    )

    obj.read = False
    obj.save
    return HttpResponse()


@csrf_exempt
@staff_member_required
def reopen_evaluation(request, course_short_title=None):
    elaboration_id = request.POST['elaboration_id']
    elaboration = Elaboration.objects.get(pk=elaboration_id)
    evaluation = Evaluation.objects.get(submission=elaboration)
    course = evaluation.submission.challenge.course

    evaluation.submission_time = None
    evaluation.tutor = request.user
    evaluation.save()

    obj, created = Notification.objects.get_or_create(
        user=evaluation.submission.user,
        course=course,
        text=Notification.SUBMISSION_EVALUATED + evaluation.submission.challenge.title,
        image_url=evaluation.submission.challenge.image.url,
        link=reverse('Challenge:stack', args=[
                     course_short_title]) + '?id=' + str(evaluation.submission.challenge.get_stack().id)
    )
    obj.creation_time = datetime.now()
    obj.read = False
    obj.save()
    return HttpResponse()


@csrf_exempt
@staff_member_required
def set_appraisal(request, course_short_title=None):
    review_id = request.POST['review_id']
    appraisal = request.POST['appraisal']

    review = Review.objects.get(pk=review_id)
    review.appraisal = appraisal
    review.save()
    if review.appraisal == review.NOTHING:
        Notification.bad_review(review)
    else:
        Notification.enough_peer_reviews(review)
    return HttpResponse()


@csrf_exempt
@aurora_login_required()
@staff_member_required
def search(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)

    selected_challenge = request.POST['selected_challenge']
    selected_user = request.POST['selected_user'].split()[0]
    selected_tag = request.POST['selected_tag']

    challenges = []
    if(selected_challenge != 'task...'):
        challenges = Challenge.objects.filter(title=selected_challenge[:(
            request.POST['selected_challenge'].rindex('(') - 1)], course=course)
    else:
        challenges = Challenge.objects.filter(course=course)

    user = []
    if(selected_user != 'user...'):
        user = AuroraUser.objects.filter(username=selected_user)
        request.session['display_points'] = "true"
    else:
        user = AuroraUser.objects.all()
        request.session['display_points'] = "false"

    if(selected_tag != 'tag...'):
        aurorauser_ct = ContentType.objects.get_for_model(AuroraUser)
        tagged_items = TaggedItem.objects.filter(
            content_type=aurorauser_ct, tag__name=selected_tag)
        tagged_user_ids = []
        for ti in tagged_items:
            if not tagged_user_ids.__contains__(ti.content_object):
                tagged_user_ids.append(ti.content_object.id)

        tagged_user = AuroraUser.objects.filter(id__in=tagged_user_ids)
        user = user & tagged_user

    elaborations = []
    if Elaboration.search(challenges, user):
        elaborations = list(Elaboration.search(challenges, user))

    # store selected elaborations in session
    request.session['elaborations'] = serializers.serialize(
        'json', elaborations)
    request.session['selection'] = 'search'
    request.session['selected_challenge'] = selected_challenge
    request.session['selected_user'] = selected_user
    request.session['selected_tag'] = selected_tag

    return evaluation(request, course_short_title)


@aurora_login_required()
@staff_member_required
def autocomplete_challenge(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)
    term = request.GET.get('term', '')
    challenges = Challenge.objects.all().filter(
        title__istartswith=term, course=course)
    titles = [challenge.title + ' (' + str(challenge.get_sub_elab_count()) + '/' + str(challenge.get_elab_count()) + ')'
              for challenge in challenges]
    response_data = json.dumps(titles, ensure_ascii=False)
    return HttpResponse(response_data, content_type='application/json; charset=utf-8')


@aurora_login_required()
@staff_member_required
def autocomplete_user(request, course_short_title=None):
    term = request.GET.get('term', '')
    studies = AuroraUser.objects.all().filter(
        Q(username__istartswith=term) | Q(first_name__istartswith=term) | Q(last_name__istartswith=term) | Q(
            nickname__istartswith=term))
    names = [(studi.username + ' ' + studi.nickname + ' ' +
              studi.first_name + ' ' + studi.last_name) for studi in studies]
    response_data = json.dumps(names, ensure_ascii=False)
    return HttpResponse(response_data, content_type='application/json; charset=utf-8')


@aurora_login_required()
@staff_member_required
def load_reviews(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)
    if not 'elaboration_id' in request.GET:
        return False

    elaboration = Elaboration.objects.get(
        pk=request.GET.get('elaboration_id', ''))
    reviews = Review.objects.filter(
        elaboration=elaboration, submission_time__isnull=False)

    return render(request, 'task.html', {'elaboration': elaboration, 'reviews': reviews, 'stack': 'stack', 'course': course})


@aurora_login_required()
@staff_member_required
def load_task(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)
    if not 'elaboration_id' in request.GET:
        return False

    elaboration = Elaboration.objects.get(
        pk=request.GET.get('elaboration_id', ''))
    stack_elaborations = elaboration.user.get_stack_elaborations(
        elaboration.challenge.get_stack())
    reviews = Review.objects.filter(
        elaboration=elaboration, submission_time__isnull=False)

    return render(request, 'task_s.html', {'stack_elaborations': stack_elaborations, 'elaboration': elaboration, 'reviews': reviews, 'stack': 'stack', 'course': course})


@require_POST
@csrf_exempt
@aurora_login_required()
@staff_member_required
def review_answer(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)

    data = request.body.decode(encoding='UTF-8')
    data = json.loads(data)

    user = request.user
    answers = data['answers']
    elab_id_from_client = data['elab']

    review = Review.objects.create(
        elaboration_id=elab_id_from_client, reviewer_id=user.id)

    review.appraisal = data['appraisal']
    review.submission_time = datetime.now()
    review.save()
    for answer in answers:
        question_id = answer['question_id']
        text = answer['answer']
        review_question = ReviewQuestion.objects.get(pk=question_id)
        ReviewAnswer(
            review=review, review_question=review_question, text=text).save()
    if review.appraisal == review.NOTHING:
        Notification.bad_review(review)
    else:
        Notification.enough_peer_reviews(review)
    # update overview
    elaborations = Elaboration.get_missing_reviews(course)
    if type(elaborations) == list:
        elaborations.sort(key=lambda elaboration: elaboration.submission_time)
    else:
        elaborations = elaborations.order_by('submission_time')
    request.session['elaborations'] = serializers.serialize(
        'json', elaborations)

    if review.elaboration.is_reviewed_2times():
        evaluation_url = reverse('Evaluation:home', args=[course_short_title])
    else:
        evaluation_url = reverse('Evaluation:detail', args=[course_short_title])\
            + "?elaboration_id=" + str(review.elaboration.id)

    return HttpResponse(evaluation_url)


@aurora_login_required()
@staff_member_required
def reviewlist(request, course_short_title=None):
    elaboration = Elaboration.objects.get(
        pk=request.session.get('elaboration_id', ''))
    reviews = Review.objects.filter(reviewer=elaboration.user, submission_time__isnull=False).order_by(
        'elaboration__challenge__id')

    return render(request, 'reviewlist.html', {'reviews': reviews})


@aurora_login_required()
@staff_member_required
def search_user(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)
    if request.GET:
        user = AuroraUser.objects.get(pk=request.GET['id'])
        elaborations = user.get_course_elaborations(course)

        # sort elaborations by submission time
        if type(elaborations) == list:
            elaborations.sort(
                key=lambda elaboration: elaboration.submission_time)
        else:
            elaborations = elaborations.order_by('submission_time')

        # store selected elaborations in session
        request.session['elaborations'] = serializers.serialize(
            'json', elaborations)
        request.session['selection'] = 'search'

    return evaluation(request, course_short_title)


# TODO: Do we really want to submit the users current list to server and
# then sort it there?
@aurora_login_required()
@staff_member_required
def sort(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)

    elaborations = []
    for serialized_elaboration in serializers.deserialize('json', request.session.get('elaborations', {})):
        elaborations.append(serialized_elaboration.object)

    if request.GET.get('data', '') == "date_asc":
        elaborations.sort(key=lambda elaboration: elaboration.submission_time)
    if request.GET.get('data', '') == "date_desc":
        elaborations.sort(
            key=lambda elaboration: elaboration.submission_time, reverse=True)
    if request.GET.get('data', '') == "elab_asc":
        elaborations.sort(key=lambda elaboration: elaboration.challenge.title)
    if request.GET.get('data', '') == "elab_desc":
        elaborations.sort(
            key=lambda elaboration: elaboration.challenge.title, reverse=True)
    if request.GET.get('data', '') == "post_asc":
        elaborations.sort(
            key=lambda elaboration: elaboration.get_last_post_date())
    if request.GET.get('data', '') == "post_desc":
        elaborations.sort(
            key=lambda elaboration: elaboration.get_last_post_date(), reverse=True)

    # store selected elaborations in session
    request.session['elaborations'] = serializers.serialize(
        'json', elaborations)
    request.session['count'] = len(elaborations)

    data = {
        'overview_html': render_to_string('overview.html', context={'elaborations': elaborations, 'course': course}, request=request),
        'menu_html': render_to_string('menu.html', context={
            'count_' + request.session.get('selection', ''): request.session.get('count', '0'),
            'stabilosiert_' + request.session.get('selection', ''): 'stabilosiert', 'course': course,
        }, request=request),
        'selection': request.session['selection']
    }

    return HttpResponse(json.dumps(data))

# TODO: Do we really want to submit the users current list to server and
# then sort it there?
@aurora_login_required()
@staff_member_required
def sort_new(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)

    elaborations = []
    for serialized_elaboration in serializers.deserialize('json', request.session.get('elaborations', {})):
        elaborations.append(serialized_elaboration.object)

    if request.GET.get('data', '') == "date_asc":
        elaborations.sort(key=lambda elaboration: elaboration.submission_time)
    if request.GET.get('data', '') == "date_desc":
        elaborations.sort(
            key=lambda elaboration: elaboration.submission_time, reverse=True)
    if request.GET.get('data', '') == "elab_asc":
        elaborations.sort(key=lambda elaboration: elaboration.challenge.title)
    if request.GET.get('data', '') == "elab_desc":
        elaborations.sort(
            key=lambda elaboration: elaboration.challenge.title, reverse=True)
    if request.GET.get('data', '') == "post_asc":
        elaborations.sort(
            key=lambda elaboration: elaboration.get_last_post_date())
    if request.GET.get('data', '') == "post_desc":
        elaborations.sort(
            key=lambda elaboration: elaboration.get_last_post_date(), reverse=True)

    # store selected elaborations in session
    request.session['elaborations'] = serializers.serialize(
        'json', elaborations)
    request.session['count'] = len(elaborations)

    data = {
        'overview_html': render_to_string('overview_new.html', {'elaborations': elaborations, 'course': course}, RequestContext(request)),
        'menu_html': render_to_string('menu.html', {
            'count_' + request.session.get('selection', ''): request.session.get('count', '0'),
            'stabilosiert_' + request.session.get('selection', ''): 'stabilosiert', 'course': course,
        }, RequestContext(request)),
        'selection': request.session['selection']
    }

    return HttpResponse(json.dumps(data))


@aurora_login_required()
def get_points(request, user, course):
    is_correct_user_request = request.user.id == user.id
    is_staff_request = request.user.is_staff
    if not (is_correct_user_request or is_staff_request):
        return HttpResponseForbidden()
    data = {}
    data['course'] = course
    course_ids = CourseUserRelation.objects.filter(
        user=user).values_list('course', flat=True)
    courses = Course.objects.filter(id__in=course_ids)
    data['courses'] = courses
    data['review_evaluation_data'] = {}
    data['review_evaluation_data'][
        'helpful_review_evaluations'] = ReviewEvaluation.get_helpful_review_evaluations(user, course)
    data['review_evaluation_data'][
        'good_review_evaluations'] = ReviewEvaluation.get_good_review_evaluations(user, course)
    data['review_evaluation_data'][
        'bad_review_evaluations'] = ReviewEvaluation.get_bad_review_evaluations(user, course)
    data['review_evaluation_data'][
        'negative_review_evaluations'] = ReviewEvaluation.get_negative_review_evaluations(user, course)

    data['review_evaluation_data'][
        'review_evaluation_percent'] = ReviewEvaluation.get_review_evaluation_percent(user, course)
    data['review_evaluation_data'][
        'reviews_missing_evaluation'] = ReviewEvaluation.get_unevaluated_reviews(user, course)
    data['review_evaluation_data']['number_of_unevaluated_reviews'] = len(
        data['review_evaluation_data']['reviews_missing_evaluation'])

    data['stacks'] = []
    for course in courses:
        stack_data = {}
        course_stacks = Stack.objects.all().filter(course=course)
        stack_data['course_title'] = course.title
        stack_data['course_stacks'] = []
        evaluated_points_earned_total = 0
        evaluated_points_available_total = 0
        submitted_points_available_total = 0
        started_points_available_total = 0
        for stack in course_stacks:
            is_submitted = stack.get_final_challenge().submitted_by_user(user)
            is_evaluated = stack.is_evaluated(user)
            is_started = stack.get_first_challenge().is_started(user)
            is_blocked = stack.is_blocked(user)
            points_available = stack.get_points_available()
            points_earned = stack.get_points_earned(user)
            stack_data['course_stacks'].append({
                'stack': stack,
                'is_started': is_started,
                'is_submitted': is_submitted,
                'is_evaluated': is_evaluated,
                'is_blocked': is_blocked,
                'points_earned': points_earned,
                'points_available': points_available,
                'status': stack.get_status_text(user),
            })
            if is_evaluated:
                # skip adding available points to totals for evaluations with 0
                # points
                if points_earned == 0:
                    continue
                evaluated_points_earned_total += points_earned
                evaluated_points_available_total += points_available
                continue
            if is_submitted:
                submitted_points_available_total += points_available
                continue
            if is_started and not is_blocked:
                started_points_available_total += points_available

        user = AuroraAuthenticationBackend.get_user(
            AuroraAuthenticationBackend(), user.id)

        stack_data[
            'evaluated_points_earned_total'] = evaluated_points_earned_total
        stack_data[
            'evaluated_points_available_total'] = evaluated_points_available_total
        stack_data[
            'submitted_points_available_total'] = submitted_points_available_total
        stack_data[
            'started_points_available_total'] = started_points_available_total
        # stack_data['lock_period'] = stack.get_final_challenge().is_in_lock_period(user, course)

        stack_data[
            'extra_points_earned_with_reviews'] = user.extra_points_earned_with_reviews(course)
        stack_data[
            'extra_points_earned_with_comments'] = user.extra_points_earned_with_comments(course)
        stack_data[
            'extra_points_earned_by_rating_reviews'] = user.extra_points_earned_by_rating_reviews(course)

        stack_data['total_extra_points_earned'] = stack_data['extra_points_earned_with_reviews'] + \
            stack_data['extra_points_earned_with_comments'] + \
            stack_data['extra_points_earned_by_rating_reviews']

        data['stacks'].append(stack_data)

    return data


@csrf_exempt
@staff_member_required
def similarities(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)

    elaboration_id = request.session.get('elaboration_id', '')

    doc = Document.get_doc_from_elaboration_id(elaboration_id)
    not_checked = False
    if doc:
        if Result.objects.filter(doc_id=doc.id).count() == 0:
            not_checked = True
    else:
        not_checked = True

    suspicion_list = Suspicion.suspicion_list_by_request(request, course)\
        .filter(suspect_doc__elaboration_id=elaboration_id)

    count = suspicion_list.count()

    context = {
        'not_checked': not_checked,
        'course': course,
        'suspicions': suspicion_list,
        'suspicion_states': SuspicionState.choices(),
        'current_suspicion_state_filter': int(request.GET.get('state', -1)),
        'suspicions_count': count,
        'enable_state_filter': False,
        'open_new_window': True,
    }

    return render(request, 'plagcheck_suspicions.html', context)


@csrf_exempt
@staff_member_required
def plagcheck_suspicions(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)

    suspicion_list = Suspicion.suspicion_list_by_request(request, course)

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

    request.session['selection'] = 'plagcheck_suspicions'
    request.session['count'] = count

    return render(request, 'evaluation.html', {
        'overview': render_to_string('plagcheck_suspicions.html', context=context, request=request),
        'course': course,
        'stabilosiert_plagcheck_suspicions': 'stabilosiert',
        'count_plagcheck_suspicions': count,
        'selection': request.session['selection'],
    })


@csrf_exempt
@staff_member_required
def plagcheck_compare(request, course_short_title=None, suspicion_id=None):
    course = Course.get_or_raise_404(short_title=course_short_title)

    suspicion = Suspicion.objects.get(pk=suspicion_id)

    (prev_suspicion_id, next_suspicion_id) = suspicion.get_prev_next(
        state=SuspicionState.SUSPECTED.value,
        #suspect_doc__submission_time__range=(course.start_date, course.end_date),
        suspect_doc__submission_time__gt=course.start_date,
    )

    try:
        similar_elaboration = suspicion.similar_doc.elaboration
        suspect_elaboration = suspicion.suspect_doc.elaboration
    except Elaboration.DoesNotExist:
        similar_elaboration = None
        suspect_elaboration = None

    context = {
        'course': course,
        'suspicion': suspicion,
        'suspicion_states': SuspicionState.states(),
        'suspicion_states_class': SuspicionState.__members__,
        'next_suspicion_id': next_suspicion_id,
        'prev_suspicion_id': prev_suspicion_id,
        'similar_elaboration': similar_elaboration,
        'suspect_elaboration': suspect_elaboration
    }

    # number of suspicious documents
    suspicions_count = Suspicion.objects.filter(
        state=SuspicionState.SUSPECTED.value).count()

    return render(request, 'evaluation.html', {
        'detail_html': render_to_string('plagcheck_compare.html', context=context, request=request),
        'course': course,
        'stabilosiert_plagcheck_suspicions': 'stabilosiert',
        'count_plagcheck_suspicions': suspicions_count,
    })


@csrf_exempt
@staff_member_required
@require_POST
def plagcheck_compare_save_state(request, course_short_title=None, suspicion_id=None):
    suspicion = Suspicion.objects.get(pk=suspicion_id)

    new_state = request.POST.get('suspicion_state_selection', None)

    suspicion.state_enum = new_state

    suspicion.save()

    return redirect('Evaluation:plagcheck_compare', course_short_title=course_short_title, suspicion_id=suspicion_id)
