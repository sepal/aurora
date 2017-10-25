from django.db import models
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType

class Review(models.Model):
    elaboration = models.ForeignKey('Elaboration.Elaboration', on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    submission_time = models.DateTimeField(null=True)
    reviewer = models.ForeignKey('AuroraUser.AuroraUser', on_delete=models.CASCADE)
    chosen_by = models.CharField(max_length=100, null=True, blank=True, default='random')
    tags = TaggableManager()
    extra_review_question_answer = models.TextField(default='')

    NOTHING = 'N'
    FAIL = 'F'
    SUCCESS = 'S'
    AWESOME = 'A'
    APPRAISAL_CHOICES = (
        (NOTHING, 'Not even trying'),
        (FAIL, 'Fail'),
        (SUCCESS, 'Success'),
        (AWESOME, 'Awesome'),
    )
    appraisal = models.CharField(max_length=1, choices=APPRAISAL_CHOICES, null=True)

    def __unicode__(self):
        return str(self.id)


    def is_evaluated(self):
        return ReviewEvaluation.objects.filter(review=self).count() > 0

    def get_content_type_id(self):
        return ContentType.objects.get_for_model(self).id

    def add_tags_from_text(self, text):
        tags = text.split(',');
        tags = [tag.lower().strip() for tag in tags]
        self.tags.add(*tags)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    @staticmethod
    def get_open_review(challenge, user):
        open_reviews = Review.objects.filter(elaboration__challenge=challenge, submission_time__isnull=True,
                                             reviewer=user)
        if open_reviews:
            return open_reviews[0]
        else:
            return None


class ReviewEvaluation(models.Model):
    review = models.ForeignKey('Review.Review', on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('AuroraUser.AuroraUser', on_delete=models.CASCADE)

    HELPFUL= 'P'
    GOOD = 'D'
    BAD = 'B'
    NEGATIVE = 'N'

    APPRAISAL_CHOICES = (
        (HELPFUL, 'Helpful Review'),
        (GOOD, 'Good Review'),
        (BAD, 'Bad Review'),
        (NEGATIVE, 'Negative Review'),
    )
    appraisal = models.CharField(max_length=1, choices=APPRAISAL_CHOICES, default='D')

    @staticmethod
    def get_helpful_review_evaluations(user, course):
        return ReviewEvaluation.objects.filter(review__reviewer=user, review__elaboration__challenge__course=course,
                                               appraisal=ReviewEvaluation.HELPFUL).count()

    @staticmethod
    def get_good_review_evaluations(user, course):
        return ReviewEvaluation.objects.filter(review__reviewer=user, review__elaboration__challenge__course=course,
                                               appraisal=ReviewEvaluation.GOOD).count()

    @staticmethod
    def get_bad_review_evaluations(user, course):
        return ReviewEvaluation.objects.filter(review__reviewer=user, review__elaboration__challenge__course=course,
                                               appraisal=ReviewEvaluation.BAD).count()

    @staticmethod
    def get_negative_review_evaluations(user, course):
        return ReviewEvaluation.objects.filter(review__reviewer=user, review__elaboration__challenge__course=course,
                                               appraisal=ReviewEvaluation.NEGATIVE).count()
    @staticmethod
    def get_review_evaluation_percent(user, course):
        number_of_reviews = Review.objects.filter(elaboration__user=user, elaboration__challenge__course=course, submission_time__isnull=False).count()
        number_of_review_evaluations = ReviewEvaluation.objects.filter(user=user, review__elaboration__challenge__course=course).count()
        if number_of_reviews == 0:
            return 0
        else:
            return number_of_review_evaluations/number_of_reviews

    @staticmethod
    def get_unevaluated_reviews(user, course):
        review_ids = Review.objects.values_list('id', flat=True).filter(elaboration__user=user, elaboration__challenge__course=course, submission_time__isnull=False)
        rated_review_ids = ReviewEvaluation.objects.values_list('review_id', flat=True).filter(user=user, review__elaboration__challenge__course=course)
        missing_ratings_ids = list(set(review_ids)-set(rated_review_ids))

        return Review.objects.filter(id__in=missing_ratings_ids)

class ReviewConfig(models.Model):
    # in hours
    candidate_offset_min = models.IntegerField(default=0)
    candidate_offset_max = models.IntegerField(default=0)

    @staticmethod
    def get_candidate_offset_min():
        config = ReviewConfig.objects.all()
        if config.count() == 0:
            return 0
        else:
            return config[0].candidate_offset_min

    @staticmethod
    def get_candidate_offset_max():
        config = ReviewConfig.objects.all()
        if config.count() == 0:
            return 0
        else:
            return config[0].candidate_offset_max

    @staticmethod
    def setup():
        ReviewConfig.objects.create(candidate_offset_min = 23, candidate_offset_max = 120)
