from django.http import JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from .models import Thread, Post, PostVote, Group, UserGroup, UserHistory, UserHistoryPost
from Course.models import Course
from .utils import get_rendered_votes_sum
from django_markup.markup import formatter


@login_required
def index(request, course_short_title):
    course = Course.get_or_raise_404(course_short_title)

    if request.user.is_superuser:
        threads = Thread.objects.filter(course=course)
    else:
        threads = Thread.objects.filter(group__usergroup__user=request.user, course=course)

    return render(request, 'diskurs/index.html', {'threads': threads, 'course': course})


@login_required
def thread(request, course_short_title, thread_id):
    course = Course.get_or_raise_404(course_short_title)
    thread_object = get_object_or_404(Thread, pk=thread_id)

    if thread_object.course != course:
        raise Http404("Thread does not exist")

    user_group = UserGroup.objects.filter(group__thread=thread_object, user=request.user).first()

    if user_group:
        thread_object.filter_group_id = user_group.group_id
    else:
        return redirect('diskurs:choose_group', course_short_title=course_short_title, thread_id=thread_id)

    user_history = UserHistory.objects.filter(user=request.user, thread=thread_object).first()

    if not user_history:
        user_history = UserHistory()
        user_history.thread = thread_object
        user_history.user = request.user
        user_history.save()

    viewed_posts = user_history.userhistorypost_set.values_list('post_id', flat=True)

    for post in thread_object.filtered_first_post.filtered_post_set.all():
        if post.id not in viewed_posts:
            user_history.add_post_id_to_history(post.id)

    return render(request, 'diskurs/thread.html', {'thread': thread_object,
                                                   'expanded_posts': [thread_object.filtered_first_post.id],
                                                   'last_post_id': thread_object.filtered_first_post.id,
                                                   'viewed_posts': viewed_posts, 'course': course})


@login_required
def thread_group(request, course_short_title, thread_id, group_id):
    course = Course.get_or_raise_404(course_short_title)
    thread_object = get_object_or_404(Thread, pk=thread_id)

    if thread_object.course != course:
        raise Http404("Thread does not exist")

    if request.user.is_superuser:
        group = get_object_or_404(Group, pk=group_id)

        if group.thread_id != int(thread_id):
            return redirect('diskurs:choose_group', course_short_title=course_short_title, thread_id=thread_id)

        thread_object.filter_group_id = group_id

    else:
        user_group = UserGroup.objects.filter(group__thread=thread_object, user=request.user).first()

        if user_group:
            thread_object.filter_group_id = user_group.group_id
        else:
            return redirect('diskurs:choose_group', course_short_title=course_short_title, thread_id=thread_id)

    user_history = UserHistory.objects.filter(user=request.user, thread=thread_object).first()

    if not user_history:
        user_history = UserHistory()
        user_history.thread = thread_object
        user_history.user = request.user
        user_history.save()

    viewed_posts = user_history.userhistorypost_set.values_list('post_id', flat=True)

    for post in thread_object.filtered_first_post.filtered_post_set.all():
        if post.id not in viewed_posts:
            user_history.add_post_id_to_history(post.id)

    return render(request, 'diskurs/thread.html', {'thread': thread_object,
                                                   'expanded_posts': [thread_object.filtered_first_post.id],
                                                   'last_post_id': thread_object.filtered_first_post.id,
                                                   'viewed_posts': viewed_posts, 'course': course})


@login_required
def thread_post(request, course_short_title, thread_id, post_id):
    course = Course.get_or_raise_404(course_short_title)
    thread_object = get_object_or_404(Thread, pk=thread_id)

    if thread_object.course != course:
        raise Http404("Thread does not exist")

    if request.user.is_superuser:
        return redirect('diskurs:choose_group', course_short_title=course_short_title, thread_id=thread_id)

    user_group = UserGroup.objects.filter(group__thread=thread_object, user=request.user).first()

    if user_group:
        thread_object.filter_group_id = user_group.group_id
    else:
        return redirect('diskurs:choose_group', course_short_title=course_short_title, thread_id=thread_id)

    post = Post.objects.get(id=post_id)
    last_post_id = post.id
    expanded_posts = list()
    rendered_posts = list()
    expanded_posts.append(post.id)
    rendered_posts.extend(post.filtered_post_set.values_list('id', flat=True))

    while post.parent_post is not None:
        post = post.parent_post
        expanded_posts.append(post.id)
        rendered_posts.extend(post.filtered_post_set.values_list('id', flat=True))

    user_history = UserHistory.objects.filter(user=request.user, thread=thread_object).first()

    if not user_history:
        user_history = UserHistory()
        user_history.thread = thread_object
        user_history.user = request.user
        user_history.save()

        user_history.add_post_to_history(thread_object.filtered_first_post, True)

    viewed_posts = user_history.userhistorypost_set.values_list('post_id', flat=True)

    for rendered_post_id in rendered_posts:
        if rendered_post_id not in viewed_posts:
            user_history.add_post_id_to_history(rendered_post_id)

    return render(request, 'diskurs/thread.html', {'thread': thread_object, 'expanded_posts': expanded_posts,
                                                   'last_post_id': last_post_id, 'viewed_posts': viewed_posts,
                                                   'course': course})


@login_required
def thread_group_post(request, course_short_title, thread_id, post_id, group_id):
    course = Course.get_or_raise_404(course_short_title)
    thread_object = get_object_or_404(Thread, pk=thread_id)

    if thread_object.course != course:
        raise Http404("Thread does not exist")

    if request.user.is_superuser:
        group = get_object_or_404(Group, pk=group_id)

        if group.thread_id != int(thread_id):
            return redirect('diskurs:choose_group', course_short_title=course_short_title, thread_id=thread_id)

        thread_object.filter_group_id = group_id
    else:
        user_group = UserGroup.objects.filter(group__thread=thread_object, user=request.user).first()

        if user_group:
            thread_object.filter_group_id = user_group.group_id
        else:
            return redirect('diskurs:choose_group', course_short_title=course_short_title, thread_id=thread_id)

    post = Post.objects.get(id=post_id)
    last_post_id = post.id
    expanded_posts = list()
    rendered_posts = list()
    expanded_posts.append(post.id)
    rendered_posts.extend(post.filtered_post_set.values_list('id', flat=True))

    while post.parent_post is not None:
        post = post.parent_post
        expanded_posts.append(post.id)
        rendered_posts.extend(post.filtered_post_set.values_list('id', flat=True))

    user_history = UserHistory.objects.filter(user=request.user, thread=thread_object).first()

    if not user_history:
        user_history = UserHistory()
        user_history.thread = thread_object
        user_history.user = request.user
        user_history.save()

    viewed_posts = user_history.userhistorypost_set.values_list('post_id', flat=True)

    for rendered_post_id in rendered_posts:
        if rendered_post_id not in viewed_posts:
            user_history.add_post_id_to_history(rendered_post_id)

    return render(request, 'diskurs/thread.html', {'thread': thread_object, 'expanded_posts': expanded_posts,
                                                   'last_post_id': last_post_id, 'viewed_posts': viewed_posts,
                                                   'course': course})


@login_required
def post_list(request, course_short_title, thread_id, post_id):
    try:
        course = Course.objects.get(short_title=course_short_title)
        thread_object = Thread.objects.get(pk=thread_id)

        if thread_object.course != course:
            return JsonResponse({
                'error': True,
                'message': 'Invalid ID provided!'
            })

        post = Post.objects.get(pk=post_id)
        last_id = int(request.GET.get('last_id', 0))

        if request.user.is_superuser:
            posts = Post.objects.filter(parent_post_id=post_id, id__gt=last_id).order_by('id')
            rendered_posts = Post.objects.filter(parent_post_id=post_id).order_by('id')

        else:
            user_group = UserGroup.objects.filter(group__thread=thread_object, user=request.user).first()

            if user_group and (user_group.group_id == post.group_id or not post.group_id):
                rendered_posts = Post.objects.filter(parent_post_id=post_id, group_id=user_group.group_id)\
                    .order_by('id')
                posts = Post.objects.filter(parent_post_id=post_id, id__gt=last_id, group_id=user_group.group_id)\
                    .order_by('id')
            else:
                return JsonResponse({
                    'success': True,
                    'posts': '',
                })

        user_history = UserHistory.objects.filter(user=request.user, thread=thread_object).first()

        if user_history:
            viewed_posts = user_history.userhistorypost_set.values_list('post_id', flat=True)
            rendered_post_ids = rendered_posts.values_list('id', flat=True)

            for rendered_post_id in rendered_post_ids:
                if rendered_post_id not in viewed_posts:
                    user_history.add_post_id_to_history(rendered_post_id)
        else:
            viewed_posts = list()

        if posts.count() > 0:

            depth = 1
            while post.parent_post is not None:
                post = post.parent_post
                depth += 1

            template = loader.get_template('diskurs/post_list.html')
            context = RequestContext(request, {
                'posts': posts,
                'depth': depth,
                'thread': thread_object,
                'viewed_posts': viewed_posts,
                'course': course,
            })

            return JsonResponse({
                'success': True,
                'posts': template.render(context),
                'new_last_id': posts.last().id,
            })
        else:
            return JsonResponse({
                'success': True,
                'posts': '',
            })

    except ValueError:
        return JsonResponse({
            'error': True,
            'message': 'Invalid ID provided!'
        })


@login_required
def post_group_list(request, course_short_title, thread_id, post_id, group_id):
    try:
        course = Course.objects.get(short_title=course_short_title)
        thread_object = Thread.objects.get(pk=thread_id)

        if thread_object.course != course:
            return JsonResponse({
                'error': True,
                'message': 'Invalid ID provided!'
            })

        post = Post.objects.get(pk=post_id)
        last_id = int(request.GET.get('last_id', 0))

        if request.user.is_superuser:
            posts = Post.objects.filter(parent_post_id=post_id, id__gt=last_id, group_id=group_id).order_by('id')
            rendered_posts = Post.objects.filter(parent_post_id=post_id, group_id=group_id).order_by('id')

            thread_object.filter_group_id = group_id

        else:
            user_group = UserGroup.objects.filter(group__thread=thread_object, user=request.user).first()

            if user_group and (user_group.group_id == post.group_id or not post.group_id):
                rendered_posts = Post.objects.filter(parent_post_id=post_id, group_id=user_group.group_id)\
                    .order_by('id')
                posts = Post.objects.filter(parent_post_id=post_id, id__gt=last_id, group_id=user_group.group_id)\
                    .order_by('id')
            else:
                return JsonResponse({
                    'success': True,
                    'posts': '',
                })

        user_history = UserHistory.objects.filter(user=request.user, thread=thread_object).first()

        if user_history:
            viewed_posts = user_history.userhistorypost_set.values_list('post_id', flat=True)
            rendered_post_ids = rendered_posts.values_list('id', flat=True)

            for rendered_post_id in rendered_post_ids:
                if rendered_post_id not in viewed_posts:
                    user_history.add_post_id_to_history(rendered_post_id)
        else:
            viewed_posts = list()

        if posts.count() > 0:

            depth = 1
            while post.parent_post is not None:
                post = post.parent_post
                depth += 1

            template = loader.get_template('diskurs/post_list.html')
            context = RequestContext(request, {
                'posts': posts,
                'depth': depth,
                'thread': thread_object,
                'viewed_posts': viewed_posts,
                'course': course,
            })

            return JsonResponse({
                'success': True,
                'posts': template.render(context),
                'new_last_id': posts.last().id,
            })
        else:
            return JsonResponse({
                'success': True,
                'posts': '',
            })

    except ValueError:
        return JsonResponse({
            'error': True,
            'message': 'Invalid ID provided!'
        })


@login_required
def new_post(request, course_short_title, thread_id):
    try:
        course = Course.objects.get(short_title=course_short_title)
        thread_object = Thread.objects.get(id=thread_id)

        if thread_object.course != course:
            return JsonResponse({
                'error': True,
                'message': 'Invalid ID provided!'
            })

        parent_post_id = int(request.POST.get('parent_post_id', 0))
        last_id = int(request.POST.get('last_id', 0))
        content = request.POST.get('content', '')

        if len(content) > 0:
            if parent_post_id > 0:
                parent_post = Post.objects.get(id=parent_post_id)
                post = Post()
                post.content = request.POST.get('content', '')
                post.parent_post = parent_post
                post.user = request.user

                if parent_post.group_id:
                    post.group_id = parent_post.group_id
                else:
                    user_group = UserGroup.objects\
                        .filter(group__thread_id=thread_id, user_id=request.user.id)\
                        .first()
                    post.group_id = user_group.group_id

                depth = 1

                while parent_post.parent_post is not None:
                    parent_post = parent_post.parent_post
                    depth += 1

                if thread_object.first_post_id == parent_post.id:
                    post.save()

                    if request.user.is_superuser:
                        posts = Post.objects.filter(parent_post_id=parent_post_id, id__gt=last_id)\
                                        .order_by('id')
                    else:
                        posts = Post.objects\
                            .filter(parent_post_id=parent_post_id, id__gt=last_id, group_id=post.group_id)\
                            .order_by('id')

                    user_history = UserHistory.objects.filter(user=request.user, thread=thread_object).first()

                    if user_history:
                        viewed_posts = list(user_history.userhistorypost_set.values_list('post_id', flat=True))

                        if post.id not in viewed_posts:
                            user_history.add_post_id_to_history(post.id)
                            viewed_posts.append(post.id)

                        for new_post_object in posts:
                            if new_post_object.id not in viewed_posts:
                                user_history.add_post_id_to_history(new_post_object.id)

                        user_history.add_post_id_to_history(post.id)

                    template = loader.get_template('diskurs/post_list.html')
                    context = RequestContext(request, {
                        'posts': posts,
                        'depth': depth,
                        'thread': thread_object,
                        'viewed_posts': viewed_posts,
                        'course': course,
                    })

                    return JsonResponse({
                        'success': True,
                        'posts': template.render(context),
                        'new_last_id': posts.last().id,
                    })

                else:
                    return JsonResponse({
                        'error': True,
                        'message': 'Invalid post ID provided!'
                    })
            else:
                return JsonResponse({
                    'error': True,
                    'message': 'Invalid post ID provided!'
                })
        else:
            return JsonResponse({
                'error': True,
                'message': 'No content provided!'
            })
    except ValueError:
        return JsonResponse({
                'error': True,
                'message': 'Invalid post ID provided!'
            })


@login_required
def new_group_post(request, course_short_title, thread_id, group_id):
    try:
        course = Course.objects.get(short_title=course_short_title)
        thread_object = Thread.objects.get(id=thread_id)

        if thread_object.course != course:
            return JsonResponse({
                'error': True,
                'message': 'Invalid ID provided!'
            })

        parent_post_id = int(request.POST.get('parent_post_id', 0))
        last_id = int(request.POST.get('last_id', 0))
        content = request.POST.get('content', '')

        if len(content) > 0:
            if parent_post_id > 0:
                parent_post = Post.objects.get(id=parent_post_id)
                post = Post()
                post.content = request.POST.get('content', '')
                post.parent_post = parent_post
                post.user = request.user

                if parent_post.group_id:
                    post.group_id = parent_post.group_id
                else:
                    if request.user.is_superuser:
                        post.group_id = group_id
                    else:
                        user_group = UserGroup.objects\
                            .filter(group__thread_id=thread_id, user_id=request.user.id)\
                            .first()
                        post.group_id = user_group.group_id

                depth = 1

                while parent_post.parent_post is not None:
                    parent_post = parent_post.parent_post
                    depth += 1

                if thread_object.first_post_id == parent_post.id:
                    post.save()

                    if request.user.is_superuser:
                        posts = Post.objects.filter(parent_post_id=parent_post_id, id__gt=last_id, group_id=group_id)\
                                        .order_by('id')
                        thread_object.filter_group_id = group_id
                    else:
                        posts = Post.objects\
                            .filter(parent_post_id=parent_post_id, id__gt=last_id, group_id=post.group_id)\
                            .order_by('id')

                    user_history = UserHistory.objects.filter(user=request.user, thread=thread_object).first()

                    if user_history:
                        viewed_posts = list(user_history.userhistorypost_set.values_list('post_id', flat=True))

                        if post.id not in viewed_posts:
                            user_history.add_post_id_to_history(post.id)
                            viewed_posts.append(post.id)

                        for new_post_object in posts:
                            if new_post_object.id not in viewed_posts:
                                user_history.add_post_id_to_history(new_post_object.id)

                        user_history.add_post_id_to_history(post.id)

                    template = loader.get_template('diskurs/post_list.html')
                    context = RequestContext(request, {
                        'posts': posts,
                        'depth': depth,
                        'thread': thread_object,
                        'viewed_posts': viewed_posts,
                        'course': course,
                    })

                    return JsonResponse({
                        'success': True,
                        'posts': template.render(context),
                        'new_last_id': posts.last().id,
                    })

                else:
                    return JsonResponse({
                        'error': True,
                        'message': 'Invalid post ID provided!'
                    })
            else:
                return JsonResponse({
                    'error': True,
                    'message': 'Invalid post ID provided!'
                })
        else:
            return JsonResponse({
                'error': True,
                'message': 'No content provided!'
            })
    except ValueError:
        return JsonResponse({
                'error': True,
                'message': 'Invalid post ID provided!'
            })


@login_required
def preview_post(request, course_short_title):
    try:
        content = request.POST.get('content', '')

        if len(content) > 0:
            return JsonResponse({
                'success': True,
                'content': formatter(content, filter_name='markdown_giffer'),
            })
        else:
            return JsonResponse({
                'error': True,
                'message': 'No content provided!'
            })
    except ValueError:
        return JsonResponse({
                'error': True,
                'message': 'Invalid post ID provided!'
            })


@login_required
def upvote_post(request, course_short_title, thread_id, post_id):
    try:
        if int(post_id) > 0:
            post = Post.objects.get(id=post_id)

            if not post.deleted:
                try:
                    post_vote = PostVote.objects.get(post_id=post_id, user_id=request.user)

                    if post_vote.value == 1:
                        post_vote.value = 0
                        post_vote.save()

                        return JsonResponse({
                            'removed': True,
                            'sum': get_rendered_votes_sum(Post.objects.get(id=post_id).sum_votes)
                        })

                except PostVote.DoesNotExist:
                    post_vote = PostVote()
                    post_vote.post_id = post_id
                    post_vote.user = request.user

                post_vote.value = 1
                post_vote.save()

                return JsonResponse({
                    'success': True,
                    'sum': get_rendered_votes_sum(Post.objects.get(id=post_id).sum_votes)
                })

            else:
                return JsonResponse({
                    'error': True,
                    'message': 'You cannot vote for a deleted post!'
                })

        else:
            return JsonResponse({
                'error': True,
                'message': 'Invalid post ID provided!'
            })

    except ValueError:
        return JsonResponse({
                'error': True,
                'message': 'Invalid post ID provided!'
            })


@login_required
def downvote_post(request, course_short_title, thread_id, post_id):
    try:
        if int(post_id) > 0:
            post = Post.objects.get(id=post_id)

            if not post.deleted:
                try:
                    post_vote = PostVote.objects.get(post_id=post_id, user_id=request.user)

                    if post_vote.value == -1:
                        post_vote.value = 0
                        post_vote.save()

                        return JsonResponse({
                            'removed': True,
                            'sum': get_rendered_votes_sum(Post.objects.get(id=post_id).sum_votes)
                        })

                except PostVote.DoesNotExist:
                    post_vote = PostVote()
                    post_vote.post_id = post_id
                    post_vote.user = request.user

                post_vote.value = -1
                post_vote.save()

                return JsonResponse({
                    'success': True,
                    'sum': get_rendered_votes_sum(Post.objects.get(id=post_id).sum_votes)
                })

            else:
                return JsonResponse({
                    'error': True,
                    'message': 'You cannot vote for a deleted post!'
                })

        else:
            return JsonResponse({
                'error': True,
                'message': 'Invalid post ID provided!'
            })

    except ValueError:
        return JsonResponse({
                'error': True,
                'message': 'Invalid post ID provided!'
            })


@login_required
def delete_post(request, course_short_title, thread_id, post_id):
    try:
        if int(post_id) > 0:
            post = Post.objects.get(id=post_id)

            if post.user == request.user or request.user.is_superuser:
                if post.parent_post_id:
                    post.deleted = True
                    post.save()

                    template = loader.get_template('diskurs/thread/post/content_deleted.html')
                    context = RequestContext(request, {
                        'post': post,
                    })

                    return JsonResponse({
                        'success': True,
                        'content': template.render(context),
                    })
                else:
                    return JsonResponse({
                        'error': True,
                        'message': 'You cannot delete the top post!'
                    })
            else:
                return JsonResponse({
                    'error': True,
                    'message': 'You are not allowed to delete the post!'
                })
        else:
            return JsonResponse({
                'error': True,
                'message': 'Invalid post ID provided!'
            })

    except ValueError:
        return JsonResponse({
                'error': True,
                'message': 'Invalid post ID provided!'
            })


@login_required
@transaction.atomic
def choose_group(request, course_short_title, thread_id):
    course = Course.get_or_raise_404(course_short_title)
    thread_object = get_object_or_404(Thread, pk=thread_id)

    if thread_object.course != course:
        raise Http404("Thread does not exist")

    groups = Group.objects.filter(thread_id=thread_id).order_by('id')
    empty_group_id = 0

    for group in groups:
        if group.usergroup_set.count() < thread_object.members_in_group:
            empty_group_id = group.id
            break

    if empty_group_id == 0:

        group = Group()
        group.thread_id = thread_id
        group.save()

        groups = Group.objects.filter(thread_id=thread_id).order_by('id')

        empty_group_id = groups.last().id

    if request.user.is_superuser:
        return render(request, 'diskurs/thread/choose_group.html', {'groups': groups, 'thread': thread_object, 'course': course})

    if not UserGroup.objects.filter(group__thread_id=thread_id, user_id=request.user).exists():

        user_group = UserGroup()
        user_group.group_id = empty_group_id
        user_group.user_id = request.user.id
        user_group.save()

    return redirect('diskurs:thread', course_short_title=course_short_title, thread_id=thread_id)


@login_required
@transaction.atomic
def choose_group_set(request, course_short_title, thread_id, group_id):
    course = Course.get_or_raise_404(course_short_title)
    group_object = get_object_or_404(Group, pk=group_id)

    if group_object.thread.course != course:
        raise Http404("Thread does not exist")

    if group_object.thread_id == int(thread_id):

        if request.user.is_superuser:
            return redirect('diskurs:thread_group', course_short_title=course_short_title, thread_id=thread_id, group_id=group_id)

        return redirect('diskurs:choose_group', course_short_title=course_short_title, thread_id=thread_id)

    return redirect('diskurs:thread', course_short_title=course_short_title, thread_id=thread_id)