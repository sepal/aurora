from django.conf import settings


class PlagCheckSettings(object):
    similarity_threshold = settings.PLAGCHECK.get('similarity_threshold', 50)
    minimal_match_count = settings.PLAGCHECK.get('minimal_match_count', 10)
    database = settings.PLAGCHECK.get('database', 'plagcheck')
    suspicion_filters = settings.PLAGCHECK.get('suspicion_filters', [])
