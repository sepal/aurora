from datetime import datetime, timedelta
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Count, Min
from django.contrib.contenttypes.models import ContentType
from random import randint

from Comments.models import Comment
from Evaluation.models import Evaluation
from Review.models import Review, ReviewConfig
from FileUpload.models import UploadFile
from ReviewAnswer.models import ReviewAnswer
from collections import Counter
from taggit.managers import TaggableManager
from pprint import pprint
from Course.models import *
from random import randint
import logging


logger = logging.getLogger('review')

class Elaboration(models.Model):
    challenge = models.ForeignKey('Challenge.Challenge')
    user = models.ForeignKey('AuroraUser.AuroraUser')
    creation_time = models.DateTimeField(auto_now_add=True)
    elaboration_text = models.TextField(default='')
    revised_elaboration_text = models.TextField(default='')
    revised_elaboration_changelog = models.TextField(default='')
    most_helpful_other_user = models.IntegerField(null=True)
    submission_time = models.DateTimeField(null=True)
    tags = TaggableManager()
    comments = GenericRelation(Comment)

    def __str__(self):
        return str(self.id)

    def is_started(self):
        if self.elaboration_text:
            return True
        if UploadFile.objects.filter(elaboration=self).exists():
            return True
        return False

    def is_submitted(self):
        if self.submission_time:
            return True
        return False

    def is_evaluated(self):
        evaluation = self.get_evaluation()
        if evaluation:
            if evaluation.submission_time:
                return True
        return False

    def get_evaluation(self):
        evaluation = Evaluation.objects.filter(submission=self)
        if evaluation.exists():
            return evaluation[0]
        return None

    def number_of_reviews(self):
        return Review.objects.filter(elaboration=self, submission_time__isnull=False).count()

    def number_of_reviews_with_feedback(self):
        count = 0
        for review in Review.objects.filter(elaboration=self, submission_time__isnull=False):
            if review.is_evaluated():
                count += 1
        return count

    def is_reviewed_2times(self):
        if self.number_of_reviews() < 2:
            return False
        return True

    def is_reviewed_3times(self):
        if self.number_of_reviews() < 3:
            return False
        return True

    def is_reviewed_1times(self):
        if self.number_of_reviews() < 1:
            return False
        return True

    def is_older_3days(self):
        if not self.is_submitted():
            return False
        if self.submission_time + timedelta(3) > datetime.now():
            return False
        return True

    def get_challenge_elaborations(self):
        elaborations = Elaboration.objects.filter(challenge=self.challenge, submission_time__isnull=False)
        if elaborations.exists():
            return elaborations
        return False

    def get_others(self):
        elaborations = (
            Elaboration.objects
            .filter(challenge=self.challenge, submission_time__isnull=False, user__is_staff=False)
            .exclude(pk=self.id)
        )
        return elaborations

    def can_be_revised(self):
        if self.is_evaluated():
            return False

        if not self.is_reviewed_1times():
            return False

        final_challenge = self.challenge.get_final_challenge()
        if not final_challenge:
            return False

        final_challenge_elaboration = final_challenge.get_elaboration(self.user)
        if final_challenge_elaboration and final_challenge_elaboration.is_submitted():
            return False

        return True

    def has_revision(self):
        if self.elaboration_text != self.revised_elaboration_text or self.revised_elaboration_changelog:
            return True

    def get_content_type_id(self):
        return ContentType.objects.get_for_model(self).id

    def add_tags_from_text(self, text):
        tags = text.split(',');
        tags = [tag.lower().strip() for tag in tags]
        self.tags.add(*tags)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    @staticmethod
    def get_sel_challenge_elaborations(challenge):
        elaborations = (
            Elaboration.objects
            .filter(challenge=challenge, submission_time__isnull=False)
        )
        return elaborations

    @staticmethod
    def get_course_sel_challenge_elaborations(challenge):
        elaborations = (
            Elaboration.objects
            .filter(challenge=challenge, submission_time__isnull=False)
        )
        return elaborations

    @staticmethod
    def get_course_sel_challenge_user_elaborations(challenge, user):
        elaborations = (
            Elaboration.objects
            .filter(challenge=challenge, user=user, submission_time__isnull=False)
        )
        return elaborations

    @staticmethod
    def search(challenges, user):
        elaborations = (
            Elaboration.objects
            .filter(challenge__in=challenges, user__in=user, submission_time__isnull=False)
        )
        return elaborations

    @staticmethod
    def get_missing_reviews(course):
        from Challenge.models import Challenge

        final_challenge_ids = Challenge.get_course_final_challenge_ids(course)
        missing_reviews = (
            Elaboration.objects
            .filter(submission_time__lte=datetime.now() - timedelta(days=1), user__is_staff=False,
                    challenge__course=course)
            .annotate(num_reviews=Count('review'))
            .exclude(challenge__id__in=final_challenge_ids)
        )
        final_elaborations = []
        for elaboration in missing_reviews:
            if elaboration.num_reviews < 2:
                final_elaborations.append(elaboration.id)
            else:
                if Review.objects.filter(elaboration=elaboration, submission_time__isnull=False).count() < 2:
                    final_elaborations.append(elaboration.id)

        missing_reviews = Elaboration.objects.filter(id__in=final_elaborations)
        return missing_reviews

    @staticmethod
    def get_extra_reviews(user, course):
        from Challenge.models import Challenge

        user_submitted_challenge_ids = Elaboration.objects.filter(user_id=user.id, submission_time__isnull=False).values_list('challenge_id', flat=True)

        final_challenge_ids = Challenge.get_course_final_challenge_ids(course)
        already_written_review_elaboration_ids = Review.objects.filter(reviewer_id=user.id).values_list('elaboration_id', flat=True)

        missing_reviews = (
            Elaboration.objects
                .annotate(num_reviews=Count('review'))
                .filter(challenge__id__in=user_submitted_challenge_ids,
                        submission_time__isnull=False,
                        user__is_staff=False,
                        challenge__course=course,
                        num_reviews__lt=2)
                .exclude(challenge__id__in=final_challenge_ids)
                .exclude(id__in=already_written_review_elaboration_ids)
                .exclude(user=user)
                .order_by('num_reviews', 'submission_time')
        )

        print(missing_reviews.query)

        missing_reviews = list(missing_reviews)
        missing_reviews.sort(key=lambda e: e.user.review_karma(course))

        # Add Open Reviews to top of list
        has_open_review = False
        open_reviews = Review.objects.filter(submission_time__isnull=True, reviewer=user)
        for review in open_reviews:
            print(review.id)
            has_open_review = True
            missing_reviews = [review.elaboration] + missing_reviews

        return { 'has_open_review': has_open_review, 'missing_reviews': missing_reviews[:7] }
        # return missing_reviews[:7]


    @staticmethod
    def get_top_level_tasks(course):
        from Challenge.models import Challenge

        final_challenge_ids = Challenge.get_course_final_challenge_ids(course)
        top_level_challenges = (
            Elaboration.objects
            .filter(challenge__id__in=final_challenge_ids, submission_time__isnull=False, user__is_staff=False)
            .annotate(evaluated=Min('evaluation__submission_time'))
            .filter(evaluated=None)
            .order_by('-submission_time')
        )
        return top_level_challenges

    @staticmethod
    def get_non_adequate_elaborations(course):
        nothing_reviews = (
            Review.objects
            .filter(appraisal=Review.NOTHING, submission_time__isnull=False)
            .prefetch_related('elaboration')
            .values_list('elaboration__id', flat=True)
        )

        non_adequate_elaborations = (
            Elaboration.objects
            .filter(id__in=nothing_reviews, submission_time__isnull=False, user__is_staff=False,
                    challenge__course=course)
        )
        return non_adequate_elaborations

    @staticmethod
    def get_non_adequate_work(course):

        """
        alle non adequate elaborations für deren final challenge es noch keine abgegebene evaluation gibt

        von allen submitted evaluations nimm den user und den stack
        für jeden stack nimm alle elaborations für den jeweiligen user

        nimm alle non adequate elaborations und exclude die vorher gefundenen elaborations
        """
        non_adequate_elaborations = Elaboration.get_non_adequate_elaborations(course).prefetch_related('challenge')

        submitted_evaluations = (
            Evaluation.objects
            .filter(submission_time__isnull=False)
            .values_list('submission__user', 'submission__challenge__stackchallengerelation__stack__id')
        )


        stack_lookup = {}
        for user, stack in submitted_evaluations:
            if not stack in stack_lookup:
                stack_lookup[stack] = [user]
            elif not user in stack_lookup[stack]:
                stack_lookup[stack].append(user)
        exclude_elaboration_ids = []
        for stack, users in stack_lookup.items():
            exclude_elaboration_ids = exclude_elaboration_ids + list(
                Elaboration.objects
                .filter(challenge__stackchallengerelation__stack__id=stack, user_id__in=users)
                .values_list('id', flat=True)
            )
        return non_adequate_elaborations.exclude(id__in=exclude_elaboration_ids)

    @staticmethod
    def get_evaluated_non_adequate_work(course):
        non_adequate_elaborations = Elaboration.get_non_adequate_elaborations(course).prefetch_related('challenge')

        submitted_evaluations = (
            Evaluation.objects
            .filter(submission_time__isnull=False)
            .values_list('submission__user', 'submission__challenge__stackchallengerelation__stack__id')
        )

        stack_loockup = {}
        for user, stack in submitted_evaluations:
            if not stack in stack_loockup:
                stack_loockup[stack] = [user]
            elif not user in stack_loockup[stack]:
                stack_loockup[stack].append(user)
        include_elaboration_ids = []
        for stack, users in stack_loockup.items():
            include_elaboration_ids = include_elaboration_ids + list(
                Elaboration.objects
                .filter(challenge__stackchallengerelation__stack__id=stack, user_id__in=users)
                .values_list('id', flat=True)
            )
        return Elaboration.objects.filter(id__in=include_elaboration_ids).filter(id__in=non_adequate_elaborations)



    @staticmethod
    def get_review_candidate(challenge, user):
        review_group = user.review_group(challenge.course)
        if review_group == 1:
            return Elaboration.get_random_review_candidate(challenge, user)
        elif review_group == 2:
            return Elaboration.get_lower_karma_review_candidate(challenge, user)
        elif review_group == 3:
            return Elaboration.get_similar_karma_review_candidate(challenge, user)

    @staticmethod
    def get_random_review_candidate(challenge, user):
        # Wait x hours before making elaborations available for review
        offset = randint(ReviewConfig.get_candidate_offset_min(), ReviewConfig.get_candidate_offset_max())
        threshold = datetime.now() - timedelta(hours=offset)

        # Exclude elaborations the user has already submitted a review for
        already_submitted_reviews_ids = (
            Review.objects
            .filter(reviewer=user, elaboration__challenge=challenge)
            .values_list('elaboration__id', flat=True)
        )

        # Get all possible candidates, ignore treshold for now because we need
        # to fall back to a random elaboration if no elaboration is old enough
        candidates = (
            Elaboration.objects
            .filter(challenge=challenge, submission_time__isnull=False, user__is_staff=False)
            .annotate(num_reviews=Count('review'))
            .exclude(user=user)
            .exclude(id__in=already_submitted_reviews_ids)
        ).order_by('num_reviews')


        # Separate candidates
        old_enough_candidates, newer_candidates = [], []
        for candidate in candidates:
            old_enough_candidates.append(candidate) if candidate.submission_time < threshold else newer_candidates.append(candidate)

        if len(old_enough_candidates) > 0:
            chosen_candidate = old_enough_candidates[0]
        elif len(newer_candidates) > 0:
            chosen_candidate = newer_candidates[0]
        else:
            # Fall back to dummy elaborations
            candidates = (
                Elaboration.objects
                .filter(challenge=challenge, submission_time__isnull=False)
                .annotate(num_reviews=Count('review'))
                .exclude(user=user)
                .exclude(id__in=already_submitted_reviews_ids)
            ).order_by('num_reviews')
            chosen_candidate = candidates[0]

        return { 'chosen_by': 'random', 'candidate': chosen_candidate }

    @staticmethod
    def get_lower_karma_review_candidate(challenge, user):
        karma_min_distance = 100
        karma_max_distance = 200

        # Exclude elaborations the user has already submitted a review for
        already_submitted_reviews_ids = (
            Review.objects
            .filter(reviewer=user, elaboration__challenge=challenge)
            .values_list('elaboration__id', flat=True)
        )

        # Find users within karma distances
        current_user       = CourseUserRelation.objects.get(course=challenge.course, active=True, user=user)
        all_possible_users = CourseUserRelation.objects.filter(course=challenge.course, active=True).order_by('review_karma')

        current_user_index = list(all_possible_users).index(current_user)

        # if current_user_index < karma_max_distance:
        #     upper_index = 100
        #     lower_index = 0
        # else:
        #     upper_index = current_user_index - karma_min_distance
        #     lower_index = current_user_index - karma_max_distance

        upper_index = current_user_index
        lower_index = 0

        possible_users = all_possible_users[lower_index:upper_index]
        possible_user_ids = [rel.user_id for rel in possible_users]

        candidates = (
            Elaboration.objects
            .filter(challenge=challenge, submission_time__isnull=False, user__is_staff=False, user_id__in=possible_user_ids)
            .annotate(num_reviews=Count('review'))
            .exclude(user=user)
            .exclude(id__in=already_submitted_reviews_ids)
        ).order_by('num_reviews')

        if candidates.count() == 0:
            logger.error('[FALLBACK] No lower-karma candidates for ' + str(user.id) + ' / ' + challenge.title)
            return Elaboration.get_random_review_candidate(challenge, user)

        if user.has_enough_special_reviews(challenge):
            logger.info('[ENOUGH REVIEWS] User ' + str(user.id) + ' has already written 2 lower-karma reviews for ' + challenge.title)
            return Elaboration.get_random_review_candidate(challenge, user)

        candidate = candidates[0]
        if candidate.number_of_reviews() >= 2:
            logger.info('[ENOUGH REVIEWS] All Elaboration already have 2 or more reviews, falling back to random')
            return Elaboration.get_random_review_candidate(challenge, user)

        user_karma      = user.review_karma(challenge.course)
        candidate_karma = candidate.user.review_karma(challenge.course)

        logger.info('[LOWER] number of lower-karma candidates: ' + str(candidates.count()) +
                    ', user/karma ' + str(user.id) + '/' + str(user_karma) +
                    ', candidate_user/candidate_karma: ' + str(candidate.user.id) + '/'  + str(candidate_karma) +
                    ', challenge: ' + challenge.title
                    )

        return { 'chosen_by': 'lower-karma', 'candidate': candidates[0] }


    @staticmethod
    def get_similar_karma_review_candidate(challenge, user):
        karma_lower_distance = 50
        karma_upper_distance = 50

        # Exclude elaborations the user has already submitted a review for
        already_submitted_reviews_ids = (
            Review.objects
            .filter(reviewer=user, elaboration__challenge=challenge)
            .values_list('elaboration__id', flat=True)
        )

        # Find users within karma distances
        current_user       = CourseUserRelation.objects.get(course=challenge.course, active=True, user=user)
        all_possible_users = CourseUserRelation.objects.filter(course=challenge.course, active=True).order_by('review_karma')

        current_user_index = list(all_possible_users).index(current_user)

        # lower_index = max(0, current_user_index - karma_lower_distance)
        # upper_index = min(all_possible_users.count(), current_user_index + karma_upper_distance)

        lower_index = 0
        upper_index = all_possible_users.count()

        possible_users = all_possible_users[lower_index:upper_index]
        possible_user_ids = [rel.user_id for rel in possible_users]

        candidates = (
            Elaboration.objects
            .annotate(num_reviews=Count('review'))
            .filter(challenge=challenge, submission_time__isnull=False, user__is_staff=False, user_id__in=possible_user_ids, num_reviews__lt=1)
            .exclude(user=user)
            .exclude(id__in=already_submitted_reviews_ids)
        )

        if candidates.count() == 0:
            logger.error('[FALLBACK] No similar-karma candidates for ' + str(user.id) + ' / ' + challenge.title)
            return Elaboration.get_random_review_candidate(challenge, user)

        if user.has_enough_special_reviews(challenge):
            logger.info('[ENOUGH REVIEWS] User ' + str(user.id) + ' has already written 2 similar-karma reviews for ' + challenge.title)
            return Elaboration.get_random_review_candidate(challenge, user)

        # Sort candidates based on review karma
        candidates = list(candidates)
        candidates.sort(key=lambda elaboration: elaboration.user.review_karma(challenge.course))

        # Separate them into users with lower and higher karma than the current user
        # The separated list are already sorted by karma
        user_karma = user.review_karma(challenge.course)
        lower_candidates, higher_candidates = [], []
        for candidate in candidates:
            lower_candidates.append(candidate) if candidate.user.review_karma(challenge.course) <= user_karma else higher_candidates.append(candidate)

        lower_candidates.reverse()

        if len(higher_candidates) == 0:
            flat_candidates = lower_candidates
        elif len(lower_candidates) == 0:
            flat_candidates = higher_candidates
        else:
            zipped_candidates = zip(lower_candidates, higher_candidates)
            zipped_candidates = list(zipped_candidates)
            flat_candidates = [item for sublist in zipped_candidates for item in sublist] # This is some serious wtf#

        if len(flat_candidates) > 1:
            # Choose one of the first 2 candidates at random
            # Candidate at [0] is the closest avaiable candidate with lower karma while candidate at [1] is the closest with higher karma
            candidate = flat_candidates[randint(0,1)]
        else:
            candidate = flat_candidates[0]

        user_karma      = user.review_karma(challenge.course)
        candidate_karma = candidate.user.review_karma(challenge.course)

        logger.info('[SIMILAR] number of similar candidates: ' + str(len(candidates)) +
                    ', user/karma ' + str(user.id) + '/' + str(user_karma) +
                    ', candidate_user/candidate_karma: ' + str(candidate.user.id) + '/'  + str(candidate_karma) +
                    ', challenge: ' + challenge.title
                    )

        return { 'chosen_by': 'similar-karma', 'candidate': candidate }

    def get_success_reviews(self):
        return Review.objects.filter(elaboration=self, submission_time__isnull=False, appraisal=Review.SUCCESS)

    def get_nothing_reviews(self):
        return Review.objects.filter(elaboration=self, submission_time__isnull=False, appraisal=Review.NOTHING)

    def get_fail_reviews(self):
        return Review.objects.filter(elaboration=self, submission_time__isnull=False, appraisal=Review.FAIL)

    def get_awesome_reviews(self):
        return Review.objects.filter(elaboration=self, submission_time__isnull=False, appraisal=Review.AWESOME)

    def get_reviews(self):
        return Review.objects.filter(elaboration=self, submission_time__isnull=False).order_by("appraisal")

    def get_lva_team_notes(self):
        reviews = (
            Review.objects
            .filter(elaboration=self, submission_time__isnull=False)
            .values_list('id', flat=True)
        )
        notes = (
            ReviewAnswer.objects
            .filter(review__id__in=reviews, review_question__visible_to_author=False).exclude(text='')
        )
        if notes.exists():
            return True
        return False

    def is_passing_peer_review(self):
        return not self.get_nothing_reviews().exists()

    @staticmethod
    def get_complaints(course):
        result = Elaboration.objects.filter(
            challenge__course=course,
            comments__seen=False
        ).distinct()

        return result

    @staticmethod
    def get_awesome(course):
        awesome_review_ids = (
            Review.objects
            .filter(appraisal=Review.AWESOME, submission_time__isnull=False)
            .values_list('elaboration__id', flat=True)
        )
        multiple_awesome_review_ids = ([k for k,v in Counter(awesome_review_ids).items() if v>1])
        awesome_elaborations = (
            Elaboration.objects
            .filter(id__in=multiple_awesome_review_ids, challenge__course=course, user__is_staff=False)
        )
        return awesome_elaborations

    @staticmethod
    def get_awesome_challenge(course, challenge):
        awesome_review_ids = (
            Review.objects
            .filter(appraisal=Review.AWESOME, submission_time__isnull=False)
            .values_list('elaboration__id', flat=True)
        )
        multiple_awesome_review_ids = ([k for k,v in Counter(awesome_review_ids).items() if v>1])
        awesome_elaborations = (
            Elaboration.objects
            .filter(id__in=multiple_awesome_review_ids, challenge=challenge, challenge__course=course,
                    user__is_staff=False)
        )
        return awesome_elaborations

    @staticmethod
    def get_stack_elaborations(stack):
        elaborations = []
        for challenge in stack.get_challenges():
            for elaboration in challenge.get_elaborations():
                elaborations.append(elaboration)
        return elaborations

    @staticmethod
    def get_course_elaborations(course):
        elaborations = []
        for challenge in course.get_course_challenges():
            for elaboration in challenge.get_elaborations():
                elaborations.append(elaboration)
        return elaborations

    def get_visible_comments_count(self):
        return self.comments.filter(visibility=Comment.PUBLIC).count()

    def get_invisible_comments_count(self):
        return self.comments.filter(visibility=Comment.STAFF).count()

    def get_last_post_date(self):
        comment = self.comments.latest('post_date')
        return comment.post_date
