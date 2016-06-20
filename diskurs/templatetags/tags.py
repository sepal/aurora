from django import template

from diskurs.models import PostVote, UserHistory, Post, UserGroup

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


@register.simple_tag
def count_new_posts(thread, user):

    user_history = UserHistory.objects.filter(user=user, thread=thread)

    if user_history.count() > 0:
        if user.is_superuser:
            new_posts = Post.objects.filter(group__thread=thread).exclude(
                            id__in=user_history.first().userhistorypost_set.values_list('post_id', flat=True))\
                        .count()
        else:
            group_id = UserGroup.objects.filter(group__thread=thread, user=user).first().group_id
            new_posts = Post.objects.filter(group=group_id).exclude(
                            id__in=user_history.first().userhistorypost_set.values_list('post_id', flat=True))\
                        .count()

    else:
        if user.is_superuser:
            new_posts = Post.objects.filter(group__thread=thread).count()
        else:
            group_id = UserGroup.objects.filter(group__thread=thread, user=user).first().group_id
            new_posts = Post.objects.filter(group=group_id).count()

    if new_posts > 1:
        return "<span class=\"count\">" + str(new_posts) + "</span> new posts"
    elif new_posts > 0:
        return "<span class=\"count\">" + str(new_posts) + "</span> new post"
    else:
        return ""


@register.simple_tag
def count_new_group_posts(group, user):

    user_history = UserHistory.objects.filter(user=user, thread=group.thread_id)

    if user_history.count() > 0:
        new_posts = Post.objects.filter(group=group).exclude(
                            id__in=user_history.first().userhistorypost_set.values_list('post_id', flat=True))\
                        .count()

    else:
        new_posts = Post.objects.filter(group=group).count()

    if new_posts > 1:
        return "<span class=\"count\">" + str(new_posts) + "</span> new posts"
    elif new_posts > 0:
        return "<span class=\"count\">" + str(new_posts) + "</span> new post"
    else:
        return ""
