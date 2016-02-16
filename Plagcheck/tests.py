import os, itertools, fnmatch, random, codecs
from unittest import skip
from django.test import TestCase
from django.test.utils import override_settings

from Plagcheck.models import Reference, Result, Suspect
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
        try:
            with codecs.open(text_file, "r", encoding='utf-8', errors='ignore') as f:
                return f.read()
        except FileNotFoundError as e:
            raise FileNotFoundError("Could not find text file at %s" % text_file, e)

    @staticmethod
    def get_random_text():
        file_list = []
        for root, dirnames, filenames in os.walk(PlagcheckTestData.get_data_root_path()):
            for filename in fnmatch.filter(filenames, '*.txt'):
                file_list.append(os.path.join(root, filename))


        #file_list = glob.iglob('%s/**/*.txt' % PlagcheckTestData.get_data_root_path(), recursive=True)
        rand_index = random.randrange(0, len(file_list)-1, 1)
        return PlagcheckTestData.get_text(file_list[rand_index])


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
        text = get_text(filename)

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

    def do_pair_test(self, prefix, expected_similarity):
        ret = self.import_text("%s_src.txt" % prefix, 0)
        self.assertEqual(ret['similarity'], 0)

        ret = self.import_text("%s_susp.txt" % prefix, 1)
        self.assertGreaterEqual(ret['similarity'], expected_similarity)

    # Tests
    def test_sherlock_mod(self):
        """ Check if modification to sherlock didn't affect results """
        hashes1 = sherlock.signature_str(get_text("simple/hello_world.txt"))
        hashes2 = sherlock.signature(get_text_path("simple/hello_world.txt"))
        self.assertSequenceEqual(hashes1, hashes2)

    def test_native_simple_repeatability(self):
        """ Generate hashes of a 3 word text with sherlock directly """

        text = get_text("simple/hello_world.txt")
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
        self.assertEqual(ret['similarity'], 0)

        ret = self.import_text("simple/hello_world.txt", 1)
        self.assertEqual(ret['similarity'], 100)

        ret = self.import_text("simple/hello_world.txt", 1)
        self.assertEqual(ret['similarity'], 100)

    def test_elaboration_single_similar(self):
        """ Test if similar document is found """

        # import same text with different doc_id
        ret1 = self.import_text("simple/hello_world.txt", 0)
        ret2 = self.import_text("simple/hello_world.txt", 1)

        similarities = Reference.get_similar_elaborations(1)
        (doc_id, similar_hashes) = similarities[0]

        self.assertEqual(doc_id, ret1['doc'])
        self.assertEqual(similar_hashes, ret1['hash_count'])

    def test_elaboration_multi_similar(self):
        """ Test if similar document is found """

        # import same text with different doc_id
        ret1 = self.import_text("simple/hello_world.txt", 0)
        ret2 = self.import_text("simple/hello_world.txt", 1)
        ret3 = self.import_text("simple/hello_world.txt", 2)

        similarities = Reference.get_similar_elaborations(2)
        (doc_id, similar_hashes) = similarities[0]
        self.assertEqual(doc_id, ret1['doc'])
        self.assertEqual(similar_hashes, 3)

        (doc_id, similar_hashes) = similarities[1]
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
        self.assertEqual(suspect.percent, 75);


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