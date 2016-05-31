from django import template

from diskurs.models import PostVote

from diskurs.utils import get_rendered_votes_sum


register = template.Library()


@register.simple_tag
def is_upvoted_post(post, user):
    try:
        uservote = post.postvote_set.get(user_id=user)

        if uservote.value == 1:
            return "marked"
        else:
            return ""
    except PostVote.DoesNotExist:
        return ""


@register.simple_tag
def is_downvoted_post(post, user):
    try:
        uservote = post.postvote_set.get(user_id=user)

        if uservote.value == -1:
            return "marked"
        else:
            return ""
    except PostVote.DoesNotExist:
        return ""


@register.simple_tag
def render_votes_sum(sum):
    return get_rendered_votes_sum(sum)