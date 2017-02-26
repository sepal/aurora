from django.core.management.base import NoArgsCommand
from AuroraUser.models import  AuroraUser
from Course.models import Course, CourseUserRelation

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        courses = Course.objects.all()

        header = ['matr_nr', 'nickname', 'first_name', 'last_name', 'study_code', 'last_activity', 'statement']
        for course in courses:
            header.append("review_karma_" + course.short_title)
            header.append("extra_points_earned_with_reviews_" + course.short_title)
            header.append("extra_points_earned_with_comments_" + course.short_title)
            header.append("extra_points_earned_by_rating_reviews_" + course.short_title)
            header.append("total_extra_points_earned_" + course.short_title)

        print("\t".join(header))

        for user in AuroraUser.objects.filter(is_staff=False):
            s = "\t".join(["{}"] * 7).format(user.matriculation_number, \
                                             user.nickname, \
                                             user.first_name, \
                                             user.last_name, \
                                             user.study_code, \
                                             str(user.last_activity), \
                                             user.statement, \
                                             )
            for course in courses:
                try:
                    karma = user.review_karma(course)
                except CourseUserRelation.DoesNotExist:
                    karma = '/'

                extra_points_earned_with_reviews = user.extra_points_earned_with_reviews(course)
                extra_points_earned_with_comments = user.extra_points_earned_with_comments(course)
                extra_points_earned_by_rating_reviews = user.extra_points_earned_by_rating_reviews(course)
                total_extra_points_earned = extra_points_earned_with_comments \
                                            + extra_points_earned_with_reviews \
                                            + extra_points_earned_by_rating_reviews

                s += "\t" + "{}".format(karma)
                s += "\t" + "{}".format(extra_points_earned_with_reviews)
                s += "\t" + "{}".format(extra_points_earned_with_comments)
                s += "\t" + "{}".format(extra_points_earned_by_rating_reviews)
                s += "\t" + "{}".format(total_extra_points_earned)


            print(s)
