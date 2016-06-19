from pydoc import locate

from PlagCheck.models import Suspicion
from PlagCheck.util.settings import PlagCheckSettings


class SuspicionFilter(object):
    """
    :type suspicion: Suspicion
    """
    @staticmethod
    def filter(suspicion):
        raise NotImplementedError("subclass and implement static filter method")


def filter_suspicion(suspicion, suspicion_filters=[]):
    """Run through all given filters and determine
    if suspicion is valid or not"""

    suspicion_state = Suspicion.DEFAULT_STATE
    reason = None
    for suspicion_filter in suspicion_filters:
        filter_state = suspicion_filter.filter(suspicion)
        if filter_state is None:
            suspicion_state = None
            reason = suspicion_filter
            break
        elif filter_state.value > suspicion_state.value:
            suspicion_state = filter_state
            reason = suspicion_filter

    return suspicion_state, reason


def load_suspicion_filters():
    suspicion_filters = []

    for filter_str in PlagCheckSettings.suspicion_filters:
        filter_class = locate(filter_str)
        suspicion_filters.append(filter_class)

    return suspicion_filters
