from django.core.management.base import NoArgsCommand
from AuroraUser.models import  AuroraUser
from Course.models import Course, CourseUserRelation

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        courses = Course.objects.all()

        header = ['matr_nr', 'nickname', 'first_name', 'last_name', 'study_code', 'last_activity', 'statement']
        for course in courses:
            header.append("review_karma " + course.short_title)

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

                s += "\t" + "{}".format(karma)

            print(s)
