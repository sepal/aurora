import os, itertools, fnmatch, random, codecs
from unittest import skip
from django.test import TestCase
from django.test.utils import override_settings

from PlagCheck.models import Reference, Result, Suspicion, SuspicionState
from PlagCheck import tasks
from ddt import ddt, data

from Elaboration.models import Elaboration
from Challenge.models import Challenge
from AuroraUser.models import AuroraUser
from Course.models import Course

from PlagCheck.util.settings import PlagCheckSettings
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
    def import_text(self, filename, doc_id=None, user=None, challenge=None, is_new=True):
        text = PlagcheckTestData.get_text(filename)

        if not user:
            user = self.user

        if not challenge:
            challenge = self.challenge

        ret = dict()

        ret['elaboration'] = Elaboration.objects.create(challenge=challenge, user=user, elaboration_text=text)
        ret['result'] = Result.objects.get(doc_id=ret['elaboration'].id)
        ret['suspicions'] = Suspicion.objects.filter(doc_id=ret['elaboration'].id)

        return ret

        #return tasks.check(doc=text,
        #                   doc_id=doc_id,
        #                   doc_version=0,
        #                   doc_type="default_type",
        #                   username=user.nickname,
        #                   is_new=False)

    def insert_random_texts(self, count):
        for i in range(0, count):
            self.import_text(PlagcheckTestData.get_random_text_path(), i)

    def do_pair_test(self, prefix, expected_similarity):
        ret1 = self.import_text("%s_src.txt" % prefix)

        self.assertEqual(len(ret1['suspicions']), 0)

        if expected_similarity > PlagCheckSettings.similarity_threshold:

            ret2 = self.import_text("%s_susp.txt" % prefix)
            self.assertGreaterEqual(ret2['suspicions'][0].similarity, expected_similarity)

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

        ret = self.import_text("simple/hello_world.txt")

        self.assertEqual(ret['result'].hash_count, 3)

    def test_repeatability(self):
        """Import a 3 words text twice and check if hashes match"""

        ret1 = self.import_text("simple/hello_world.txt")
        first_hashes = hashes(ret1['elaboration'].id)

        ret2 = self.import_text("simple/hello_world.txt")
        second_hashes = hashes(ret2['elaboration'].id)

        self.assertSequenceEqual(first_hashes, second_hashes)

    def test_hello_world_update(self):
        """ Import a 3 word text 3 times and check similarity """

        ret = self.import_text("simple/hello_world.txt")
        self.assertEqual(len(ret['suspicions']), 0)

        ret = self.import_text("simple/hello_world.txt")
        self.assertEqual(len(ret['suspicions']), 1)

        ret = self.import_text("simple/hello_world.txt")
        self.assertEqual(len(ret['suspicions']), 2)

    #@skip("remove this")
    def test_elaboration_single_similar(self):
        """ Test if similar document is found """

        # import same text with different doc_id
        ret1 = self.import_text("simple/hello_world.txt")
        ret2 = self.import_text("simple/hello_world.txt")

        similarities = Reference.get_similar_elaborations(ret2['elaboration'].id)
        (doc_id, similar_hashes, filter_id) = similarities[0]

        self.assertEqual(doc_id, ret1['result'].doc_id)
        self.assertEqual(similar_hashes, ret1['result'].hash_count)

    def test_elaboration_multi_similar(self):
        """ Test if similar document is found """

        # import same text with different doc_id
        ret1 = self.import_text("simple/hello_world.txt")
        ret2 = self.import_text("simple/hello_world.txt")
        ret3 = self.import_text("simple/hello_world.txt")

        similarities = Reference.get_similar_elaborations(2)
        (doc_id, similar_hashes, filter_id) = similarities[0]
        self.assertEqual(similar_hashes, 3)

        (doc_id, similar_hashes, filter_id) = similarities[1]
        self.assertEqual(similar_hashes, 3)

    def test_suspicion_single_similar(self):
        ret1 = self.import_text("princeton/princeton_001_src.txt")

        self.assertEqual(Suspicion.objects.all().count(), 0)

        ret2 = self.import_text("princeton/princeton_001_susp.txt")

        self.assertEqual(Suspicion.objects.all().count(), 1)

        suspicion = Suspicion.objects.get()

        self.assertEqual(suspicion.doc_id, ret2['elaboration'].id)
        self.assertEqual(suspicion.similar_doc_id, ret1['elaboration'].id)
        self.assertEqual(suspicion.similarity, 75)

    def test_duplicate_hash(self):
        self.import_text("simple/duplicate_hash.txt")
        self.import_text("simple/duplicate_hash.txt")
        suspicion = Suspicion.objects.get()
        self.assertEqual(suspicion.similarity, 100)

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

                self.import_text("sheffield/orig_%s.txt" % (test[1]))

                ret = self.import_text("sheffield/%s_%s.txt" % (test[0], test[1]))
                #self.assertGreaterEqual(ret['similarity'], 0)

                #print("testing %s_%s.txt against orig_%s.txt gives %i%% similarity" % (test[0], test[1], test[1], ret['similarity']))
            except UnicodeDecodeError:
                continue
