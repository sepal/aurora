import os, itertools, fnmatch, random, codecs
from unittest import skip
from django.test import TestCase
from django.test.utils import override_settings

from Plagcheck.models import Reference, Result, Suspect, SuspectFilter, SuspectState
from Plagcheck import tasks
from ddt import ddt, data

from Elaboration.models import Elaboration
from Challenge.models import Challenge
from AuroraUser.models import AuroraUser
from Course.models import Course
import sherlock # noqa

def hashes(doc_id):
    ret = list()
    for ref in Reference.objects.all().filter(doc_id=doc_id):
        ret.append(ref.hash)
    return ret

class PlagcheckTestData:
    @staticmethod
    def get_data_root_path():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "test", "data")

    @staticmethod
    def get_text_path(filename):
        return os.path.join(PlagcheckTestData.get_data_root_path(), filename)

    @staticmethod
    def get_text(filename):
        text_file = PlagcheckTestData.get_text_path(filename)
        with codecs.open(text_file, "r", encoding='utf-8', errors='ignore') as f:
            return f.read()

    @staticmethod
    def get_random_text_path():
        file_list = []
        for root, dirnames, filenames in os.walk(PlagcheckTestData.get_data_root_path()):
            for filename in fnmatch.filter(filenames, '*.txt'):
                file_list.append(os.path.join(root, filename))

        rand_index = random.randrange(0, len(file_list)-1, 1)
        return file_list[rand_index]

    @staticmethod
    def get_random_text():
        return PlagcheckTestData.get_text(PlagcheckTestData.get_random_text_path())

@ddt
@override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
class PlagCheckTestCase(TestCase):

    # Fixture
    def setUp(self):

        self.course = Course.objects.create(title="plagcheck", short_title="plagcheck", description="desc")
        self.user = AuroraUser.objects.create(nickname="plagcheck-test")
        self.challenge = Challenge.objects.create(title="plagcheck-challange", subtitle="subtitle", description="desc", course=self.course)

        # self.challanges = Challenge.objects.all()
        # self.users = AuroraUser.objects.all()

    # Helpers
    def import_text(self, filename, doc_id, user=None, challenge=None, is_new=True):
        text = PlagcheckTestData.get_text(filename)

        if not user:
            user = self.user

        if not challenge:
            challange = self.challenge

        # Elaboration.objects.create(challenge=challenge, user=user, elaboration_text=text)
        return tasks.check(doc=text,
                           doc_id=doc_id,
                           doc_version=0,
                           doc_type="default_type",
                           username=user.nickname,
                           is_new=False)

    def insert_random_texts(self, count):
        for i in range(0, count):
            self.import_text(PlagcheckTestData.get_random_text_path(), i)

    def do_pair_test(self, prefix, expected_similarity):
        ret = self.import_text("%s_src.txt" % prefix, 0)

        self.assertEqual(len(Suspect.objects.all()), 0)

        result = Result.objects.get(doc_id=0)

        self.assertEqual(result.)

        ret = self.import_text("%s_susp.txt" % prefix, 1)
        self.assertGreaterEqual(Reference.overall_similarity(1, ret['hash_count']), expected_similarity)

    # Tests
    def test_sherlock_mod(self):
        """ Check if modification to sherlock didn't affect results """
        hashes1 = sherlock.signature_str(PlagcheckTestData.get_text("simple/hello_world.txt"))
        hashes2 = sherlock.signature(PlagcheckTestData.get_text_path("simple/hello_world.txt"))
        self.assertSequenceEqual(hashes1, hashes2)

    def test_native_simple_repeatability(self):
        """ Generate hashes of a 3 word text with sherlock directly """

        text = PlagcheckTestData.get_text("simple/hello_world.txt")
        hashes1 = sherlock.signature_str(text)
        hashes2 = sherlock.signature_str(text)
        self.assertSequenceEqual(hashes1, hashes2)

    def test_task_entry(self):
        """ Import a 3 words text and check API return values """

        ret = self.import_text("simple/hello_world.txt", 0)

        self.assertEqual(ret['doc'], 0)
        self.assertEqual(ret['username'], "plagcheck-test")
        self.assertEqual(ret['doc_type'], "default_type")
        self.assertEqual(ret['hash_count'], 3)
        self.assertEqual(ret['similarity'], 0)

    def test_repeatability(self):
        """Import a 3 words text twice and check if hashes match"""

        self.import_text("simple/hello_world.txt", 0)
        first_hashes = hashes(0)

        self.import_text("simple/hello_world.txt", 1)
        second_hashes = hashes(1)

        self.assertSequenceEqual(first_hashes, second_hashes)

    def test_hello_world_update(self):
        """ Import a 3 word text twice and check similarity """

        ret = self.import_text("simple/hello_world.txt", 0)
        self.assertEqual(ret['similarity'], 0)

        ret = self.import_text("simple/hello_world.txt", 1)
        self.assertEqual(ret['similarity'], 100)

    def test_hello_world_update(self):
        """ Import a 3 word text 3 times and check similarity """

        ret = self.import_text("simple/hello_world.txt", 0)
        self.assertEqual(Reference.overall_similarity(0, ret['hash_count']), 0)

        ret = self.import_text("simple/hello_world.txt", 1)
        self.assertEqual(Reference.overall_similarity(1, ret['hash_count']), 100)

        ret = self.import_text("simple/hello_world.txt", 1)
        self.assertEqual(Reference.overall_similarity(1, ret['hash_count']), 100)

    def test_elaboration_single_similar(self):
        """ Test if similar document is found """

        # import same text with different doc_id
        ret1 = self.import_text("simple/hello_world.txt", 0)
        ret2 = self.import_text("simple/hello_world.txt", 1)

        similarities = Reference.get_similar_elaborations(1)
        (doc_id, similar_hashes, filter_id) = similarities[0]

        self.assertEqual(doc_id, ret1['doc'])
        self.assertEqual(similar_hashes, ret1['hash_count'])

    def test_elaboration_multi_similar(self):
        """ Test if similar document is found """

        # import same text with different doc_id
        ret1 = self.import_text("simple/hello_world.txt", 0)
        ret2 = self.import_text("simple/hello_world.txt", 1)
        ret3 = self.import_text("simple/hello_world.txt", 2)

        similarities = Reference.get_similar_elaborations(2)
        (doc_id, similar_hashes, filter_id) = similarities[0]
        self.assertEqual(doc_id, ret1['doc'])
        self.assertEqual(similar_hashes, 3)

        (doc_id, similar_hashes, filter_id) = similarities[1]
        self.assertEqual(doc_id, ret2['doc'])
        self.assertEqual(similar_hashes, 3)

    def test_suspect_single_similar(self):
        self.import_text("princeton/princeton_001_src.txt", 0)

        self.assertEqual(Suspect.objects.all().count(), 0)

        self.import_text("princeton/princeton_001_susp.txt", 1)

        self.assertEqual(Suspect.objects.all().count(), 1)

        suspect = Suspect.objects.get()

        self.assertEqual(suspect.doc_id, 1)
        self.assertEqual(suspect.similar_to_id, 0)
        self.assertEqual(suspect.percent, 75)

    def test_duplicate_hash(self):
        self.import_text("simple/duplicate_hash.txt", 0)
        self.import_text("simple/duplicate_hash.txt", 1)
        suspect = Suspect.objects.get()
        self.assertEqual(suspect.percent, 100)

    def test_filter(self):
        self.import_text("simple/hello_world.txt", 0)
        SuspectFilter.objects.create(doc_id=0)
        self.import_text("simple/hello_world.txt", 1)
        suspect = Suspect.objects.get()
        self.assertEqual(suspect.percent, 100)
        self.assertEqual(suspect.state, SuspectState.AUTO_FILTERED.value)

    def test_filter_small_diff(self):
        self.import_text("simple/der_kommentar.txt", 0)
        SuspectFilter.objects.create(doc_id=0)
        self.import_text("simple/das_kommentar.txt", 1)
        suspect = Suspect.objects.get()
        self.assertGreater(suspect.percent, 50)
        self.assertEqual(suspect.state, SuspectState.AUTO_FILTERED.value)

    def test_filter_small_diff_reverse(self):
        self.import_text("simple/das_kommentar.txt", 0)
        SuspectFilter.objects.create(doc_id=0)
        self.import_text("simple/der_kommentar.txt", 1)
        suspect = Suspect.objects.get()
        self.assertGreater(suspect.percent, 50)
        self.assertEqual(suspect.state, SuspectState.AUTO_FILTERED.value)

    def test_filter_small_diff_others(self):
        self.import_text("simple/der_kommentar.txt", 0)
        SuspectFilter.objects.create(doc_id=0)
        self.import_text("simple/der_kommentar.txt", 1)
        self.import_text("simple/der_kommentar.txt", 2)
        suspects = Suspect.objects.all()

        for suspect in suspects:
            print(str(suspect))
            self.assertEqual(suspect.state, SuspectState.AUTO_FILTERED.value)

    @skip("deprecated")
    def test_match_count(self):

        self.insert_random_texts(20)

        self.import_text("simple/match_count_bug_review.txt", 20)
        self.import_text("simple/match_count_bug_review.txt", 21)

        match_count = Reference.get_match_count(1)
        similar = Reference.get_similar_elaborations(1)

        computed_match_count = 0
        for (doc_id, similar_hashes, filter_id) in similar:
            computed_match_count += similar_hashes

        self.assertEqual(computed_match_count, match_count)

    @data(("princeton/princeton_001", 75), ("princeton/princeton_002", 30), ("princeton/princeton_003", 80))
    def test_princeton_dataset(self, value):
        """ Run test sets from https://www.princeton.edu/pr/pub/integrity/pages/plagiarism/ """

        self.do_pair_test(value[0], value[1])

    @skip("tested only when needed")
    def test_sheffield_dataset(self):
        """ Run test sets from http://ir.shef.ac.uk/cloughie/resources/plagiarism_corpus.html#Download
        taking results from http://www.cscjournals.org/library/manuscriptinfo.php?mc=IJCL-33 into account
        """

        data = list(itertools.product(["g0pA", "g0pB", "g0pC", "g0pD", "g0pE", "g1pA", "g1pB", "g1pD", "g2pA", "g2pB",
                                       "g2pC", "g2pE", "g3pA", "g3pB", "g3pC", "g4pB", "g4pC", "g4pD"],
                                      ["taska", "taskb", "taskc", "taskd", "taske"]))

        for test in data:
            try:

                self.import_text("sheffield/orig_%s.txt" % (test[1]), 0)

                ret = self.import_text("sheffield/%s_%s.txt" % (test[0], test[1]), 1)
                self.assertGreaterEqual(ret['similarity'], 0)

                print("testing %s_%s.txt against orig_%s.txt gives %i%% similarity" % (test[0], test[1], test[1], ret['similarity']))
            except UnicodeDecodeError:
                continue
