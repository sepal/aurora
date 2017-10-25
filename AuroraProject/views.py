import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.functional import cached_property
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

from AuroraProject.decorators import aurora_login_required
from Course.models import Course
from AuroraUser.models import AuroraUser
from Evaluation.models import Evaluation
from Review.models import Review
from ReviewAnswer.models import ReviewAnswer
from Elaboration.models import Elaboration
from Challenge.models import Challenge
# unused, and therefore commented out because importing app views means they
# can't import this module properly
#from Evaluation.views import get_points
#from Statistics.views import create_stat_data
#from Elaboration.views import get_extra_review_data
from Faq.models import Faq
from middleware.AuroraAuthenticationBackend import AuroraAuthenticationBackend

import logging

logger = logging.getLogger(__name__)


class CourseMixin:
    course_kwarg_name = "course_short_title"
    @cached_property
    def course(self):
        course_short_title = self.kwargs.get(self.course_kwarg_name)
        course = Course.get_or_raise_404(short_title=course_short_title)
        return course


def course_from_url(url):
    course = None
    try:
        # Match the part between '^/course/' and the following '/' in url
        match = re.search('(?<=^/course/)[^/]+', url)
        course = match.group(0)
    except IndexError:
        pass
    finally:
        return course


def course_selection(request):

    # store next_url if available inside the session
    next_url = None
    if 'next' in request.GET:
        next_url = request.GET['next']

    if next_url:
        request.session['next_url'] = next_url

    if not request.user.is_authenticated:
        if 'sKey' in request.GET:
            from AuroraUser.views import sso_auth_callback
            return sso_auth_callback(request)

    # automatically redirect the user to its course login page
    # if a next_url is defined.
    course = course_from_url(next_url)
    if next_url and course:
        try:
            print('reverse url: ' + str(reverse("User:login", args=(course, ))))
            redirect_url = reverse("User:login", args=(course, ))
        except NoReverseMatch:
            pass
        else:
            return redirect(redirect_url)

    data = {'courses': Course.objects.all(), 'next': next_url, 'debug': settings.DEBUG}
    return render(request, 'course_selection.html', data)


@aurora_login_required()
def home(request, course_short_title=None):

    user = AuroraAuthenticationBackend.get_user(AuroraAuthenticationBackend(), request.user.id)
    course = Course.get_or_raise_404(course_short_title)
    data = {}
    data['course'] = course

    # data = get_points(request, user, course)
    # data = create_stat_data(course,data)
    # data['user_is_top_reviewer'] = False
    #
    # data['number_of_extra_reviews'] = user.number_of_extra_reviews(course)
    # data['reviews_until_next_extra_point'] = user.number_of_reviews_until_next_extra_point(course)
    # data['extra_points_earned_with_reviews'] = user.extra_points_earned_with_reviews(course)
    # if user.is_top_reviewer(course):
    #     # data['number_of_extra_reviews'] = user.number_of_extra_reviews(course)
    #     # data['reviews_until_next_extra_point'] = user.number_of_reviews_until_next_extra_point(course)
    #     # data['extra_points_earned_with_reviews'] = user.extra_points_earned_with_reviews(course)
    #     data['user_is_top_reviewer'] = True
    #     # Expensive function, therefor only execute if user is top reviewer
    #     data = get_extra_review_data(user, course, data)

    data['extra_points_earned_with_comments'] = user.extra_points_earned_with_comments(course)
    data['extra_points_earned_by_rating_reviews'] = user.extra_points_earned_by_rating_reviews(course)
    data['total_extra_points_earned'] = user.total_extra_points_earned(course)
    faq_list = Faq.get_faqs(course_short_title)

    data["all_courses"] = Course.objects.all()

    return render(request, 'home.html', data)


def time_to_unix_string(time):
    if time is None:
        return str(None)

    delta = time - datetime(1970, 1, 1)
    hours = delta.days * 24
    seconds = hours * 3600
    seconds += delta.seconds
    return str(seconds)


@login_required()
@staff_member_required
def result_users(request):
    s = ""
    for user in AuroraUser.objects.filter(is_staff=False):
        s += "\t".join(["{}"] * 7).format(user.matriculation_number,
                                          user.nickname,
                                          user.first_name,
                                          user.last_name,
                                          user.study_code,
                                          time_to_unix_string(user.last_activity),
                                          user.statement)
        s += "\n"

    return HttpResponse(s, mimetype="text/plain; charset=utf-8")


@login_required()
@staff_member_required
def result_elabs_nonfinal(request):
    """
    username (mnr) TAB elabID TAB challenge-title TAB challenge-ID TAB creation time TAB submission time TAB
    reviewID 1 TAB review-verdict 1 TAB review-creation-date 1 TAB review-submission-date 1 TAB reviewID 2 TAB
    review-verdict 2 TAB review-creation-date 2 TAB review-submission-date 2 TAB usw.
    """

    final_challenge_ids = Challenge.get_final_challenge_ids()
    elabs = Elaboration.objects.exclude(challenge__id__in=final_challenge_ids).prefetch_related()

    s = ""
    for elab in elabs:
        s += "\t".join(["{}"] * 6).format(
            str(elab.user.matriculation_number),
            str(elab.id),
            elab.challenge.title,
            str(elab.challenge.id),
            time_to_unix_string(elab.creation_time),
            time_to_unix_string(elab.submission_time)
        )

        for review in Review.objects.filter(elaboration=elab):
            s += "\t" + str(review.id)
            s += "\t" + str(review.appraisal)
            s += "\t" + time_to_unix_string(review.creation_time)
            s += "\t" + time_to_unix_string(review.submission_time)

        s += "\n"

    return HttpResponse(s, mimetype="text/plain; charset=utf-8")


@login_required()
@staff_member_required
def result_elabs_final(request):
    """
    username(mnr) TAB elabID TAB challenge-title TAB challenge-ID TAB creation time TAB submission time TAB
    evaluationID TAB tutor TAB evaluation-creationdate TAB evaluation-submissiontime TAB evaluation-points
    """

    evals = Evaluation.objects.all().prefetch_related()

    s = ""
    for evaluation in evals:
        elab = evaluation.submission
        s += "\t".join(["{}"] * 11).format(
            str(elab.user.matriculation_number),
            str(elab.id),
            elab.challenge.title,
            str(elab.challenge.id),
            time_to_unix_string(elab.creation_time),
            time_to_unix_string(elab.submission_time),
            evaluation.id,
            evaluation.tutor.display_name,
            time_to_unix_string(evaluation.creation_date),
            time_to_unix_string(evaluation.submission_time),
            str(evaluation.evaluation_points)
        )

        s += "\n"

    return HttpResponse(s, mimetype="text/plain; charset=utf-8")


def get_result_reviews():
    """
    Since this is so slow (and can be too slow for a application server response, this is also being used
    as a command in Review.

    review-autor (MNr) TAB
    reviewed-elab-autor (MNr) TAB
    reviewed-elab-challenge-ID TAB
    review-creation-date TAB
    review-submission-date TAB
    länge des reviews (number of chars of all fields summiert)
    """
    reviews = Review.objects.all().prefetch_related()
    result = ""
    for review in reviews:
        answers = ReviewAnswer.objects.filter(review=review.id)
        answer_string = ""
        for answer in answers:
            answer_string += answer.text
        length = len(answer_string)

        result += "\t".join(["{}"] * 6).format(
            review.reviewer.username,
            review.elaboration.user.username,
            review.elaboration.challenge_id,
            time_to_unix_string(review.creation_time),
            time_to_unix_string(review.submission_time),
            str(length)
        )

        result += "\n"

    return result


@login_required()
@staff_member_required
def result_reviews(request):
    result = get_result_reviews()

    return HttpResponse(result, mimetype="text/plain; charset=utf-8")


@csrf_exempt
@staff_member_required
def add_tags(request, course_short_title=None):
    text = request.POST['text']
    object_id = request.POST['object_id']
    content_type_id = request.POST['content_type_id']

    content_type = ContentType.objects.get_for_id(content_type_id)
    taggable_object = content_type.get_object_for_this_type(pk=object_id)
    taggable_object.add_tags_from_text(text)

    return render(request, 'tags.html', {'tagged_object': taggable_object})


@csrf_exempt
@staff_member_required
def remove_tag(request, course_short_title=None):
    tag = request.POST['tag']
    object_id = request.POST['object_id']
    content_type_id = request.POST['content_type_id']

    content_type = ContentType.objects.get_for_id(content_type_id)
    taggable_object = content_type.get_object_for_this_type(pk=object_id)
    taggable_object.remove_tag(tag)

    return render(request, 'tags.html', {'tagged_object': taggable_object})


@login_required()
@staff_member_required
def autocomplete_tag(request, course_short_title=None):
    term = request.GET.get('term', '')
    content_type_id = request.GET['content_type_id']

    content_type = ContentType.objects.get_for_id(content_type_id)
    taggable_model = content_type.model_class()
    tags = taggable_model.tags.all().filter(
        Q(name__istartswith=term)
    )
    names = [tag.name for tag in tags]
    response_data = json.dumps(names, ensure_ascii=False)
    return HttpResponse(response_data, content_type='application/json; charset=utf-8')
