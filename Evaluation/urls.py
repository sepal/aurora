from django.conf.urls import patterns, url

import Evaluation.views

urlpatterns = [
    url(r'^$', Evaluation.views.evaluation, name='home'),
    url(r'^detail$', Evaluation.views.detail, name='detail'),
    url(r'^stack/$', Evaluation.views.stack, name='tasks'),
    url(r'^others/$', Evaluation.views.others, name='others'),
    url(r'^challenge_txt/$', Evaluation.views.challenge_txt, name='task_description'),
    url(r'^user-detail$', Evaluation.views.user_detail, name='user-detail'),
    url(r'^reviewlist/$', Evaluation.views.reviewlist, name='reviews'),
    url(r'^missing_reviews$', Evaluation.views.missing_reviews, name='missing_reviews'),
    url(r'^non_adequate_work$', Evaluation.views.non_adequate_work, name='non_adequate_work'),
    url(r'^top_level_tasks$', Evaluation.views.top_level_tasks, name='top_level_tasks'),
    url(r'^complaints$', Evaluation.views.complaints, name='complaints'),
    url(r'^questions$', Evaluation.views.questions, name='questions'),
    url(r'^awesome$', Evaluation.views.awesome, name='awesome'),
    url(r'^user$', Evaluation.views.search_user, name='search_user'),

    url(r'^autocomplete_challenge/$', Evaluation.views.autocomplete_challenge),
    url(r'^autocomplete_user/$', Evaluation.views.autocomplete_user),
    url(r'^search/$', Evaluation.views.search),
    url(r'^sort$', Evaluation.views.sort),
    url(r'^set_appraisal/$', Evaluation.views.set_appraisal),
    url(r'^review_answer/$', Evaluation.views.review_answer),
    url(r'^load_reviews/$', Evaluation.views.load_reviews),
    url(r'^load_task/$', Evaluation.views.load_task),

    url(r'^start_evaluation$', Evaluation.views.start_evaluation),
    url(r'^save_evaluation/$', Evaluation.views.save_evaluation),
    url(r'^submit_evaluation/$', Evaluation.views.submit_evaluation),
    url(r'^reopen_evaluation/$', Evaluation.views.reopen_evaluation),

    url(r'^plagcheck/$', Evaluation.views.plagcheck_suspicions, name='plagcheck_suspicions'),
    url(r'^plagcheck/(?P<suspicion_id>\d+)/$', Evaluation.views.plagcheck_compare, name='plagcheck_compare'),
    url(r'^plagcheck/(?P<suspicion_id>\d+)/save_state/$', Evaluation.views.plagcheck_compare_save_state, name='plagcheck_compare_save_state'),
]
