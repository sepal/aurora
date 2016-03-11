from django import template

from diskurs.models import PostVote


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