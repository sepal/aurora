import os
import hashlib
import urllib.request
from django.contrib.auth.models import User, UserManager
from django.contrib.contenttypes.models import ContentType
from AuroraProject.settings import STATIC_ROOT, MEDIA_ROOT
from Elaboration.models import Elaboration
from django.core.files import File
from Review.models import Review, ReviewEvaluation
from Course.models import Course, CourseUserRelation
from Challenge.models import Challenge
from Comments.models import *
from Slides.models import *
from Stack.models import *

def avatar_path(instance, filename):
    name = 'avatar_%s' % instance.id
    fullname = os.path.join(instance.upload_path, name)
    if os.path.exists(fullname):
        os.remove(fullname)
    return fullname

class AuroraUser(User):
    nickname = models.CharField(max_length=100, null=True, blank=True)
    last_activity = models.DateTimeField(auto_now_add=True, blank=True)
    statement = models.TextField(blank=True)
    upload_path = 'avatar'
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True)
    matriculation_number = models.CharField(max_length=100, null=True, unique=True, blank=True)
    study_code = models.CharField(max_length=100, null=True, blank=True, default="")
    oid = models.CharField(max_length=30, null=True, unique=True, blank=True)
    tags = TaggableManager()

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def enlisted_and_active_for_course(self, course):
        try:
            CourseUserRelation.objects.get(user=self, course=course, active=True)
            return True
        except CourseUserRelation.DoesNotExist:
            return False

    def calculate_review_karma(self):
        for relation in CourseUserRelation.objects.filter(user=self):
            positive_tags = ["exceptional", "helpful", "good", ]
            questionable_tags = ["enthusiastic", ]
            negative_tags= ["min", "empty", "bad", "wrong", "leer", "offensive", "meaningless", ]

            positive_review_scale_factor = 3
            neutral_review_scale_factor  = 1
            negative_review_scale_factor = 3
            helpful_review_scale_factor  = 2

            positive_tag_scale_factor     = 2
            questionable_tag_scale_factor = 1
            negative_tag_scale_factor     = 3

            course = relation.course

            number_of_neutral_reviews  = ReviewEvaluation.objects.filter(review_id__reviewer_id=self.id, review__elaboration__challenge__course_id=course.id, appraisal='D').count()
            number_of_positive_reviews = ReviewEvaluation.objects.filter(review_id__reviewer_id=self.id, review__elaboration__challenge__course_id=course.id, appraisal='P').count()
            number_of_negative_reviews = ReviewEvaluation.objects.filter(review_id__reviewer_id=self.id, review__elaboration__challenge__course_id=course.id, appraisal='N').count()
            number_of_helpful_reviews  = Elaboration.objects.filter(most_helpful_other_user=self.id).count()

            student_reviews = Review.objects.filter(reviewer_id=self.id, elaboration_id__challenge_id__course_id=course.id)
            total_reviews = Review.objects.filter(elaboration_id__challenge_id__course_id=course.id, reviewer_id__is_staff=False).count()

            number_of_positive_tags     = student_reviews.filter(tags__name__regex=r'(' + '|'.join(positive_tags) + ')').values('tagged_items__tag_id', 'tagged_items__object_id').distinct().count()
            number_of_questionable_tags = student_reviews.filter(tags__name__regex=r'(' + '|'.join(questionable_tags) + ')').values('tagged_items__tag_id', 'tagged_items__object_id').distinct().count()
            number_of_negative_tags     = student_reviews.filter(tags__name__regex=r'(' + '|'.join(negative_tags) + ')').values('tagged_items__tag_id', 'tagged_items__object_id').distinct().count()

            quality_factor_numerator = number_of_positive_reviews * positive_review_scale_factor + \
                                       number_of_neutral_reviews  * neutral_review_scale_factor  + \
                                       number_of_helpful_reviews  * helpful_review_scale_factor  + \
                                       number_of_positive_tags    * positive_tag_scale_factor

            quality_factor_denominator = quality_factor_numerator + \
                                         number_of_negative_reviews  * negative_review_scale_factor  + \
                                         number_of_negative_tags     * negative_tag_scale_factor     + \
                                         number_of_questionable_tags * questionable_tag_scale_factor


            if (quality_factor_denominator == 0 or total_reviews == 0):
                review_karma = 0.0
            else:
                quality_factor = quality_factor_numerator / quality_factor_denominator
                quantity_factor = student_reviews.count() / total_reviews
                review_karma = quantity_factor * quality_factor

            relation.review_karma = review_karma
            relation.save()

    def review_karma(self, course):
        return CourseUserRelation.objects.get(user=self, course=course).review_karma

    def is_top_reviewer(self, course):
        return CourseUserRelation.objects.get(user=self, course=course).top_reviewer

    def number_of_extra_reviews(self, course):
        return Review.objects.filter(submission_time__isnull=False, reviewer=self, chosen_by='extra_review', elaboration_id__challenge_id__course_id=course.id).count()

    def number_of_reviews_until_next_extra_point(self, course):
        return 3 - (self.number_of_extra_reviews(course) % 3)

    def extra_points_earned_with_reviews(self, course):
        return self.number_of_extra_reviews(course) // 3

    def extra_points_earned_with_comments(self, course):
        extra_points = 0
        for promoted_comment in  Comment.objects.filter(author=self, promoted=True):
            referenced_object = promoted_comment.content_object
            if isinstance(referenced_object, Course):
                if referenced_object.short_title == course.short_title:
                    extra_points += 1
            elif isinstance(referenced_object, Slide):
                if referenced_object.lecture.course.short_title == course.short_title:
                    extra_points += 1
            elif isinstance(referenced_object, Elaboration):
                if referenced_object.challenge.course.short_title == course.short_title:
                    extra_points += 1
            elif referenced_object.course.short_title == course.short_title:
                extra_points += 1

        return extra_points

    def extra_points_earned_by_rating_reviews(self, course):
        if self.has_rated_most_reviews(course):
            return 1
        return 0

    def has_rated_most_reviews(self, course):
        rated = self.number_of_reviews_rated(course)
        received = self.number_of_reviews_received(course)

        if received == 0:
            return False

        if  rated / received >= 0.8:
            return True

        return False

    def total_points_submitted(self, course):
        submitted_points = 0

        for stack in Stack.objects.all().filter(course=course):
            if stack.get_final_challenge().submitted_by_user(self):
                submitted_points += stack.get_points_available()

        return submitted_points

    def has_submitted_one_challenge_of_each_chapter(self, course):
        check = True

        for chapter in Chapter.objects.all():
            chapter_final_challenge_ids = []
            # print(chapter.id)
            for stack in Stack.objects.filter(course=course, chapter=chapter):
                chapter_final_challenge_ids.append(stack.get_final_challenge().id)

            if len(chapter_final_challenge_ids) > 0:
                # print(chapter_final_challenge_ids)
                completed_for_chapter = Elaboration.objects.filter(challenge_id__in=chapter_final_challenge_ids, user=self, submission_time__isnull=False).count()

                if completed_for_chapter == 0:
                    check = False

        return check


    def number_of_reviews_rated(self, course):
        return ReviewEvaluation.objects.filter(review__elaboration__user=self).count()

    def number_of_reviews_received(self, course):
        return Review.objects.filter(elaboration__user=self).count()

    def total_extra_points_earned(self, course):
        return self.extra_points_earned_by_rating_reviews(course) + self.extra_points_earned_with_comments(course) + self.extra_points_earned_with_reviews(course)

    def has_enough_special_reviews(self, challenge):
        return Review.objects.filter(elaboration__challenge=challenge).exclude(chosen_by='random').count() == 2

    def review_group(self, course):
        return CourseUserRelation.objects.get(user=self, course=course).review_group

    def get_elaborations(self):
        elaborations = []
        for elaboration in Elaboration.objects.filter(user=self, submission_time__isnull=False):
            elaborations.append(elaboration)
        return elaborations

    def get_reviews(self):
        return Review.objects.filter(reviewer=self)

    def get_course_elaborations(self, course):
        elaborations = []
        for elaboration in Elaboration.objects.filter(user=self, challenge__course=course, submission_time__isnull=False):
            elaborations.append(elaboration)
        return elaborations

    def get_challenge_elaboration(self, challenge):
        return challenge.get_elaboration(self)

    def get_stack_elaborations(self, stack):
        elaborations = []
        for challenge in stack.get_challenges():
            elaboration = self.get_challenge_elaboration(challenge)
            if elaboration and elaboration.is_submitted():
                elaborations.append(elaboration)
        return elaborations

    def get_gravatar(self):
        filename = "avatar_" + str(self.id)
        if not os.path.isdir(os.path.join(MEDIA_ROOT,self.upload_path)):
            os.makedirs(os.path.join(MEDIA_ROOT,self.upload_path))
        try:
            gravatarurl = "http://www.gravatar.com/avatar/" + hashlib.md5(
                self.email.lower().encode("utf-8")).hexdigest() + "?"
            gravatarurl += urllib.parse.urlencode({'d': 'monsterid', 's': str(192)})
            result = urllib.request.urlretrieve(gravatarurl)
            self.avatar.save(avatar_path(self, ''), File(open(result[0], 'rb')))
        except IOError:
            from shutil import copyfile
            copyfile(os.path.join(STATIC_ROOT, 'img', 'default_gravatar.png'), os.path.join(MEDIA_ROOT, avatar_path(self, '')))
        self.avatar = os.path.join(self.upload_path, filename)
        self.save()

    def get_content_type_id(self):
        return ContentType.objects.get_for_model(self).id

    def add_tags_from_text(self, text):
        tags = text.split(',');
        tags = [tag.lower().strip() for tag in tags]
        self.tags.add(*tags)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    @staticmethod
    def query_tagged(tags):
        return AuroraUser.objects.filter(tags__name__in=tags)

    @property
    def display_name(self):
        display_name = self.username if self.nickname is None else self.nickname
        return display_name
