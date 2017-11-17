from datetime import datetime
import json
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import transaction
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
from PlagCheck.views import render_to_string_compare_view, render_to_string_suspicions_view
from middleware.AuroraAuthenticationBackend import AuroraAuthenticationBackend
from functools import lru_cache


class EvaluationView(CourseMixin, TemplateView):
    mode_template_names = {
        "overview": "evaluation.html",
        "export": "evaluation_export.html",
    }
    overview_template_name = "overview.html"
    valid_ordering_fields = [
        "submission_time",
        "creation_time",
    ]
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
        self.request.session['selection'] = self.selection_name
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
            "selected_challenge": self.request.session.get("selected_challenge"),
            "selected_tag": self.request.session.get("selected_tag"),
            "selected_user": self.request.session.get("selected_user"),
        })

        return context

    def get_extra_session(self):
        return {}

    def get_order_by(self):
        order_by = self.request.GET.get("order_by", None)
        if (order_by is None or
                (not order_by.lstrip("-") in self.valid_ordering_fields)):
            return "submission_time"
        return order_by

    def get_elaborations(self):
        raise NotImplemented

    def _get_elaborations(self):
        elaborations = self.get_elaborations()

        # sort elaborations by submission time
        if type(elaborations) == list:
            elaborations.sort(
                    key=lambda elaboration: elaboration.submission_time)
        else:
            elaborations = elaborations.order_by(self.get_order_by())

        return elaborations

    def get_overview_context_data(self):
        return {
            'elaborations': self.elaborations,
            'course': self.course,
            "selection": self.selection_name,
        }




class BaseSearchView(EvaluationView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_challenge"] = self.selected_challenge
        return context

    def get_extra_session(self):
        return {
            "selected_challenge": "task..."
        }

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

questions = QuestionsView.as_view()


class SearchUserView(BaseSearchView):
    selection_name = "search_user"
    def get_elaborations(self):
        if "id" not in self.request.GET:
            raise Http404
        user = get_object_or_404(AuroraUser, pk=self.request.GET['id'])
        return user.get_course_elaborations(self.course)

search_user = SearchUserView.as_view()


class SearchView(BaseSearchView):
    selection_name = "search"
    def get_elaborations(self):
        self._set_selected()

        if (self.selected_challenge != 'task...'):
            challenges = Challenge.objects.filter(
                            title=self.selected_challenge[
                                    :(self.selected_challenge.rindex('(') - 1)],
                            course=self.course)
        else:
            challenges = Challenge.objects.filter(course=self.course)

        if(self.selected_user != 'user...'):
            user = AuroraUser.objects.filter(username=self.selected_user)
            self.request.session['display_points'] = "true"
        else:
            user = AuroraUser.objects.all()
            self.request.session['display_points'] = "false"

        if(self.selected_tag != 'tag...'):
            aurorauser_ct = ContentType.objects.get_for_model(AuroraUser)
            tagged_items = TaggedItem.objects.filter(
                content_type=aurorauser_ct, tag__name=selected_tag)
            tagged_user_ids = []
            for ti in tagged_items:
                if not tagged_user_ids.__contains__(ti.content_object):
                    tagged_user_ids.append(ti.content_object.id)

            tagged_user = AuroraUser.objects.filter(id__in=tagged_user_ids)
            user = user & tagged_user

        return Elaboration.search(challenges, user)

    def get_extra_session(self):
        return {
            "selected_challenge": self.selected_challenge,
            "selected_tag": self.selected_tag,
            "selected_user": self.selected_user,
        }

    def _set_selected(self):
        if self.request.method == "POST":
            self.selected_challenge = self.request.POST.get('selected_challenge', "task...")
            self.selected_user = self.request.POST.get('selected_user', "user...").split()[0]
            self.selected_tag = self.request.POST.get('selected_tag', "tag...")
        else:
            self.selected_challenge = self.request.session.get('selected_challenge', "task...")
            self.selected_user = self.request.session.get('selected_user', "user...")
            self.selected_tag = self.request.session.get('selected_tag', "tag...")

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

search = SearchView.as_view()


@csrf_exempt
@staff_member_required
def plagcheck_suspicions(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)

    ret_data = render_to_string_suspicions_view(request, course);

    return render(request, 'evaluation.html', {
        'overview': ret_data['html'],
        'course': course,
        'stabilosiert_plagcheck_suspicions': 'stabilosiert',
        'count_plagcheck_suspicions': ret_data['count'],
        'selection': request.session['selection'],
    })


@csrf_exempt
@staff_member_required
def plagcheck_compare(request, course_short_title=None, suspicion_id=None):
    course = Course.get_or_raise_404(short_title=course_short_title)
    ret_data = render_to_string_compare_view(request, course, suspicion_id)

    return render(request, 'evaluation.html', {
        'detail_html': ret_data['html'],
        'course': course,
        'stabilosiert_plagcheck_suspicions': 'stabilosiert',
        'count_plagcheck_suspicions': ret_data['count'],
    })


EVALUATION_VIEWS = {
    "awesome": awesome,
    "complaints": complaints,
    "final_evaluation_new": final_evaluation_new,
    "final_evaluation_top_level_tasks": final_evaluation_top_level_tasks,
    "top_level_tasks": top_level_tasks,
    "non_adequate_work": non_adequate_work,
    "missing_reviews": missing_reviews,
    "questions": questions,
    "search": search,
    "search_user": search_user,
    "plagcheck_suspicions": plagcheck_suspicions,
}


def evaluation(request, **kwargs):
    selection = request.session.get('selection', 'missing_reviews')
    view = EVALUATION_VIEWS.get(selection)
    if view is None:
        raise Http404
    return view(request, **kwargs)


@aurora_login_required()
@staff_member_required
def overview(request, course_short_title=None):
    course = Course.get_or_raise_404(short_title=course_short_title)
    elaboration = Elaboration.objects.get(pk=request.GET.get('elaboration_id'))
    user = elaboration.user
    stack = elaboration.challenge.get_stack()
    stack_challenges = stack.get_challenges()

    try:
        next_elaboration = elaboration.get_next_by_creation_time()
    except Elaboration.DoesNotExist:
        next_elaboration = None

    challenges = []
    for challenge in stack_challenges:
        challenge_data = {}
        challenge_data['challenge'] = challenge
        challenge_data['final'] = challenge.is_final_challenge()

        elaboration =  challenge.get_elaboration(user)
        challenge_data['elaboration'] = elaboration

        reviews = challenge.get_reviews_written_by_user(user)
        for review in reviews:
            review_evaluation_tutor = ReviewEvaluation.objects.filter(review=review.id, user=request.user)
            review_evaluation_student = ReviewEvaluation.objects.filter(review=review.id, user__is_staff=False)
            try:
                review.appraisal_tutor = review_evaluation_tutor.values()[0].get('appraisal')
            except IndexError:
                pass
            try:
                review.appraisal_student = review_evaluation_student.values()[0].get('appraisal')
            except:
                pass
        challenge_data['reviews'] = reviews

        challenge_data['received_reviews'] = Review.objects.filter(elaboration=elaboration, submission_time__isnull=False)
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

    params = {}
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
    if selection in ("search", "search_user"):
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

    try:
        prev = elaboration.get_previous_by_creation_time()
    except Elaboration.DoesNotExist:
        prev = None

    try:
        next = elaboration.get_next_by_creation_time()
    except Elaboration.DoesNotExist:
        next = None

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
    obj.save()
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

    with transaction.atomic():
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
def get_points(request, user, course):
    is_correct_user_request = request.user.id == user.id
    is_staff_request = request.user.is_staff
    if not (is_correct_user_request or is_staff_request):
        return HttpResponseForbidden()
    data = {}
    data['course'] = course
    courses = user.courses.all()

    data['courses'] = courses

    review_evaluation_data_students = {}
    review_evaluation_data_students['helpful_review_evaluations'] = ReviewEvaluation.get_helpful_review_evaluations(user, course)
    review_evaluation_data_students['good_review_evaluations'] = ReviewEvaluation.get_good_review_evaluations(user, course)
    review_evaluation_data_students['bad_review_evaluations'] = ReviewEvaluation.get_bad_review_evaluations(user, course)
    review_evaluation_data_students['negative_review_evaluations'] = ReviewEvaluation.get_negative_review_evaluations(user, course)
    data['review_evaluation_data_students'] = review_evaluation_data_students

    review_evaluation_data_tutors = {}
    review_evaluation_data_tutors['helpful_review_evaluations'] = ReviewEvaluation.get_helpful_review_evaluations(user, course, user_is_staff=True)
    review_evaluation_data_tutors['good_review_evaluations'] = ReviewEvaluation.get_good_review_evaluations(user, course, user_is_staff=True)
    review_evaluation_data_tutors['bad_review_evaluations'] = ReviewEvaluation.get_bad_review_evaluations(user, course, user_is_staff=True)
    review_evaluation_data_tutors['negative_review_evaluations'] = ReviewEvaluation.get_negative_review_evaluations(user, course, user_is_staff=True)
    data['review_evaluation_data_tutors'] = review_evaluation_data_tutors
    
    review_evaluation_data = {}
    review_evaluation_data['review_evaluation_percent'] = ReviewEvaluation.get_review_evaluation_percent(user, course)
    review_evaluation_data['reviews_missing_evaluation'] = ReviewEvaluation.get_unevaluated_reviews(user, course)
    review_evaluation_data['number_of_unevaluated_reviews'] = len(review_evaluation_data['reviews_missing_evaluation'])
    data['review_evaluation_data'] = review_evaluation_data

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

    options = {
        'filter_by_suspect_elaboration': elaboration_id,
        'open_new_window': True,
        'enable_filters': False,
    }

    return HttpResponse(render_to_string_suspicions_view(request, course, options)['html'])

