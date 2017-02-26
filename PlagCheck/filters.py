import re

from PlagCheck.util.filter import SuspicionFilter
from PlagCheck.util.state import SuspicionState
from PlagCheck.util.settings import PlagCheckSettings


class SimilarityThresholdFilter(SuspicionFilter):
    @staticmethod
    def filter(suspicion):
        if suspicion.similarity < PlagCheckSettings.similarity_threshold:
            return None
        return SuspicionState.SUSPECTED


class MinimalMatchCountFilter(SuspicionFilter):
    @staticmethod
    def filter(suspicion):
        if suspicion.match_count < PlagCheckSettings.minimal_match_count:
            return None
        return SuspicionState.SUSPECTED


class RevisedElaborationFilter(SuspicionFilter):
    @staticmethod
    def filter(suspicion):
        if (suspicion.suspect_doc.user_id == suspicion.similar_doc.user_id \
                or suspicion.suspect_doc.user_name == suspicion.similar_doc.user_name) \
                and suspicion.suspect_doc.elaboration_id == suspicion.similar_doc.elaboration_id \
                and suspicion.suspect_doc.is_revised != suspicion.similar_doc.is_revised:
            return None
        return SuspicionState.SUSPECTED


class SelfPlagiarismFilter(SuspicionFilter):
    @staticmethod
    def filter(suspicion):
        if suspicion.suspect_doc.user_name == suspicion.similar_doc.user_name:
            return SuspicionState.SUSPECTED_SELF_PLAGIARISM
        return SuspicionState.SUSPECTED


class DummyUserFilter(SuspicionFilter):
    @staticmethod
    def filter(suspicion):
        if re.match('^(Nickname_){0,1}[ds]\d+$', suspicion.suspect_doc.user_name):
            return None
        return SuspicionState.SUSPECTED