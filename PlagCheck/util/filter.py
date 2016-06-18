from PlagCheck.models import Suspicion


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
