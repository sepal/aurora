import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, Http404

import AuroraUser
from AuroraProject.decorators import aurora_login_required
from Course.models import Course
from Review.models import Review, ReviewEvaluation
from Elaboration.models import Elaboration
from Challenge.models import Challenge
from ReviewQuestion.models import ReviewQuestion
from ReviewAnswer.models import ReviewAnswer
from Notification.models import Notification
from Review.models import ReviewConfig

import logging
logger = logging.getLogger(__name__)


def create_context_review(request):
    data = {}
    if 'id' in request.GET:
        user = request.user
        challenge = Challenge.objects.get(pk=request.GET.get('id'))
        if not challenge.is_enabled_for_user(user):
            raise Http404
        if challenge.has_enough_user_reviews(user):
            raise Http404
        if not challenge.submitted_by_user(user):
            raise Http404
        review = Review.get_open_review(challenge, user)
        if not review:
            review_candidate = Elaboration.get_review_candidate(challenge, user)
            if review_candidate:
                review = Review(elaboration=review_candidate['candidate'], reviewer=user, chosen_by=review_candidate['chosen_by'])
                review.save()
            else:
                return data
        data['review'] = review
        data['stack_id'] = challenge.get_stack().id
        review_questions = ReviewQuestion.objects.filter(challenge=challenge).order_by("order")

        author_questions = [question for question in review_questions if question.visible_to_author == True]
        staff_questions  = [question for question in review_questions if question.visible_to_author == False]

        data['questions'] = review_questions
        data['author_questions'] = author_questions
        data['staff_questions'] = staff_questions

        extra_review_question_present = len(review.elaboration.extra_review_question) > 0
        data['extra_review_question_present'] = extra_review_question_present


    return data


@aurora_login_required()
def review(request, course_short_title):
    data = create_context_review(request)
    data['course'] = Course.get_or_raise_404(course_short_title)
    return render(request, 'review.html', data)


def create_context_extra_review(request):
    data = {}
    if 'id' in request.GET:
        user = request.user
        challenge = Challenge.objects.get(pk=request.GET.get('id'))
        elaboration = Elaboration.objects.get(pk=request.GET.get('elaboration_id'))
        if not challenge.is_enabled_for_user(user):
            raise Http404
        if not challenge.submitted_by_user(user):
            raise Http404

        review = Review.get_open_review(challenge, user)
        if not review:
            review = Review(elaboration=elaboration, reviewer=user, chosen_by='extra_review')
            review.save()

        data['review'] = review
        data['stack_id'] = challenge.get_stack().id
        review_questions = ReviewQuestion.objects.filter(challenge=challenge).order_by("order")
        data['questions'] = review_questions
    return data

@aurora_login_required()
def extra_review(request, course_short_title):
    data = create_context_extra_review(request)
    data['course'] = Course.get_or_raise_404(course_short_title)
    return render(request, 'review.html', data)


@aurora_login_required()
def review_answer(request, course_short_title):
    user = request.user
    if request.POST:
        data = request.body.decode(encoding='UTF-8')
        data = json.loads(data)
        review_id = data['review_id']
        answers = data['answers']
        try:
            review = Review.objects.get(pk=review_id)
            challenge = review.elaboration.challenge
            if not challenge.is_enabled_for_user(user):
                raise Http404
            if not review == Review.get_open_review(challenge, user):
                raise Http404
        except:
            raise Http404
        review.appraisal = data['appraisal']

        for answer in answers:
            question_id = answer['question_id']
            text = answer['answer']
            review_question = ReviewQuestion.objects.get(pk=question_id)

            # check if this answer has already been posted
            # submit button could have been pressed twice
            # there is no other way to check for this, because the parent
            # review object gets created when creating the review view
            # so we can't check it here because it would already exist.
            # get_or_create() would work here, but notifications would be sent in both cases
            if ReviewAnswer.objects.filter(review=review, review_question=review_question).exists():

                # log this incident so we can trace it down to the client. Is it IE?
                logger.error("We prevented a review to be submitted twice. Report this with client details.")
                logger.error("review_id=%i, user_id=%i, question_id=%i, review_question_id=%i" % review.id, user.id, question_id, review_question.id)
                raise Http404

            ReviewAnswer(review=review, review_question=review_question, text=text).save()
            # send notifications
        review.submission_time = datetime.now()
    
        if 'extra_review_question_answer' in data:
            review.extra_review_question_answer = data['extra_review_question_answer']

        review.save()

        try:
            if review.appraisal == review.NOTHING:
                Notification.bad_review(review)
            else:
                Notification.enough_peer_reviews(review)
        except:
            print('Could not send Notification')

    return HttpResponse()

@aurora_login_required()
def evaluate(request, course_short_title):
    user = request.user
    if not request.GET:
        raise Http404
    if not 'appraisal' in request.GET:
        raise Http404
    appraisal = request.GET['appraisal']
    if not 'review_id' in request.GET:
        raise Http404
    review_id = request.GET['review_id']
    review = Review.objects.get(id=review_id)

    if user.is_staff:
        try:
            review_evaluation = ReviewEvaluation.objects.get(user__is_staff=True, review=review)
        except ReviewEvaluation.DoesNotExist:
            review_evaluation = ReviewEvaluation(user=user, review=review, appraisal=appraisal)
            review_evaluation.save()
            update_review_karma(request, review_evaluation)
        else:
            # ReviewEvaluation already exists
            review_evaluation.user = user
            review_evaluation.appraisal = appraisal
            review_evaluation.save()
            update_review_karma(request, review_evaluation)

    else:
        review_evaluation, created = ReviewEvaluation.objects.get_or_create(user=user, review=review)
        review_evaluation.appraisal = appraisal
        review_evaluation.save()
        update_review_karma(request, review_evaluation)

    return HttpResponse()

def update_review_karma(request, review_evaluation):
    review_author = review_evaluation.review.reviewer
    review_evaluations = ReviewEvaluation.objects.filter(review_id__reviewer_id=review_author.id)
    review_evaluations_tutors = review_evaluations.filter(user__is_staff=True)
    review_evaluations_students = review_evaluations.filter(user__is_staff=False)

    total_score_tutors = calculate_total_score(review_evaluations_tutors)
    total_score_students = calculate_total_score(review_evaluations_students)

    try:
        review_karma_tutors = total_score_tutors / len(review_evaluations_tutors)
    except ZeroDivisionError:
        review_karma_tutors = 0.0

    try:
        review_karma_students = total_score_students / len(review_evaluations_students)
    except ZeroDivisionError:
        review_karma_students = 0.0

    review_author.update_review_karma(review_karma_tutors, review_karma_students)

def calculate_total_score(review_evaluations):
    total_score = 0.0
    for review_evaluation in review_evaluations:
        score = 0.0
        if review_evaluation.appraisal == 'P':  # helpful
            score = 1.0
        elif review_evaluation.appraisal == 'D':  # ok
            score = 0.5
        elif review_evaluation.appraisal == 'B':  # meaningless
            score = 0.2
        elif review_evaluation.appraisal == 'N':  # minimal
            score = 0.1
        total_score = total_score + score
    return total_score