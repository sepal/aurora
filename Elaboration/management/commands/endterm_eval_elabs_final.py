__author__ = 'queltos'

from django.core.management.base import NoArgsCommand
from Evaluation.models import Evaluation
from Stack.models import StackChallengeRelation

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        """
        username(mnr) TAB elabID TAB challenge-title TAB challenge-ID TAB creation time TAB submission time TAB
        evaluationID TAB tutor TAB evaluation-creationdate TAB evaluation-submissiontime TAB evaluation-points
        """

        evals = Evaluation.objects.all().prefetch_related()

        header = ['username', 'elaboration_id', 'challenge_title', 'chapter_id', 'course_id', 'elaboration_challenge_id', 'elaboration_creation_time', \
                  'elaboration_submission_time', 'elaboration_changelog', 'most_helpful_other_user',  \
                  'evaluation_id', 'tutor_name', 'evaluation_creation_timte', 'evaluation_submission_time', 'evaluation_points']

        print("\t".join(header))

        for eval in evals:
            elab = eval.submission
            if elab.most_helpful_other_user == None:
                most_helfpul = '/'
            else:
                most_helfpul = elab.most_helpful_other_user.matriculation_number

            s = "\t".join(["{}"] * 15).format(
                elab.user.nickname + " (" + str(elab.user.matriculation_number) + ")",
                str(elab.id),
                elab.challenge.title,
                StackChallengeRelation.objects.get(challenge=elab.challenge).stack.chapter.id,
                elab.challenge.course_id,
                str(elab.challenge.id),
                str(elab.creation_time),
                str(elab.submission_time),
                elab.revised_elaboration_changelog,
                most_helfpul,
                eval.id,
                eval.tutor.display_name,
                str(eval.creation_date),
                str(eval.submission_time),
                str(eval.evaluation_points)
            )

            print(s)
