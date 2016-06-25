from enum import IntEnum

class SuspicionState(IntEnum):
    """SUSPECTED: Default state of a possible plagiarism document.
    PLAGIARISM: The suspected document is plagiarism.
    FALSE_POSITIVE: No plagiarism at all, could be improved by algorithm
    CITED: The suspected document contained a ordinary citation to the similar document.
    """

    SUSPECTED = 0
    PLAGIARISM = 1
    FALSE_POSITIVE = 2
    CITED = 3
    SUSPECTED_SELF_PLAGIARISM = 4

    @staticmethod
    def states():
        states = []
        for state in SuspicionState:
            states.append({'value': state.value, 'name': state.name})
        return states

    @staticmethod
    def choices():
        choices = ()
        for state in SuspicionState:
            choices += ((state.value, state.name),)
        return choices