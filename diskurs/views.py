from django.http import JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Thread, Post, PostVote, Group, UserGroup


@login_required
def index(request):
    threads = Thread.objects.filter(group__usergroup__user=request.user)

    return render(request, 'diskurs/index.html', {'threads': threads})


@login_required
def thread(request, thread_id):
    thread_object = get_object_or_404(Thread, pk=thread_id)

    if thread_object.use_group_logic and not request.user.has_perm('view_post'):
        user_group = UserGroup.objects.filter(group__thread=thread_object, user=request.user).first()

        if user_group:
            thread_object.filter_group_id = user_group.group_id
        else:
            return redirect('diskurs:choose_group', thread_id=thread_id)

    return render(request, 'diskurs/thread.html', {'thread': thread_object, 'expanded_posts': []})


@login_required
def thread_post(request, thread_id, post_id):
    thread_object = get_object_or_404(Thread, pk=thread_id)

    if thread_object.use_group_logic and not request.user.has_perm('view_post'):
        user_group = UserGroup.objects.filter(group__thread=thread_object, user=request.user).first()

        if user_group:
            thread_object.filter_group_id = user_group.group_id
        else:
            return redirect('diskurs:choose_group', thread_id=thread_id)

    post = Post.objects.get(id=post_id)
    last_post_id = post.id
    expanded_posts = list()
    expanded_posts.append(post.id)

    while post.parent_post is not None:
        post = post.parent_post
        expanded_posts.append(post.id)

    return render(request, 'diskurs/thread.html', {'thread': thread_object, 'expanded_posts': expanded_posts,
                                                   'last_post_id': last_post_id})


@login_required
def post_list(request, thread_id, post_id):
    try:
        thread_object = Thread.objects.get(pk=thread_id)
        post = Post.objects.get(pk=post_id)
        last_id = int(request.GET.get('last_id', 0))

        if thread_object.use_group_logic and not request.user.has_perm('view_post'):
            user_group = UserGroup.objects.filter(group__thread=thread_object, user=request.user).first()

            if user_group and (user_group == post.group_id or not post.group_id):
                posts = Post.objects.filter(parent_post_id=post_id, id__gt=last_id, group_id=user_group.group_id)\
                    .order_by('id')
            else:
                return JsonResponse({
                    'success': True,
                    'posts': '',
                })

        else:
            posts = Post.objects.filter(parent_post_id=post_id, id__gt=last_id).order_by('id')

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
def new_post(request, thread_id):
    try:
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

                thread_object = Thread.objects.get(id=thread_id)

                if parent_post.group_id:
                    post.group_id = parent_post.group_id
                else:
                    if thread_object.use_group_logic:
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

                    if thread_object.use_group_logic and not request.user.has_perm('view_post'):
                        posts = Post.objects\
                            .filter(parent_post_id=parent_post_id, id__gt=last_id, group_id=post.group_id)\
                            .order_by('id')
                    else:
                        posts = Post.objects.filter(parent_post_id=parent_post_id, id__gt=last_id)\
                                        .order_by('id')

                    template = loader.get_template('diskurs/post_list.html')
                    context = RequestContext(request, {
                        'posts': posts,
                        'depth': depth,
                        'thread': thread_object,
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
def upvote_post(request, thread_id, post_id):
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
                            'sum': Post.objects.get(id=post_id).sum_votes
                        })

                except PostVote.DoesNotExist:
                    post_vote = PostVote()
                    post_vote.post_id = post_id
                    post_vote.user = request.user

                post_vote.value = 1
                post_vote.save()

                return JsonResponse({
                    'success': True,
                    'sum': Post.objects.get(id=post_id).sum_votes
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
def downvote_post(request, thread_id, post_id):
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
                            'sum': Post.objects.get(id=post_id).sum_votes
                        })

                except PostVote.DoesNotExist:
                    post_vote = PostVote()
                    post_vote.post_id = post_id
                    post_vote.user = request.user

                post_vote.value = -1
                post_vote.save()

                return JsonResponse({
                    'success': True,
                    'sum': Post.objects.get(id=post_id).sum_votes
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
def delete_post(request, thread_id, post_id):
    try:
        if int(post_id) > 0:
            post = Post.objects.get(id=post_id)

            if post.user == request.user or request.user.has_perm('delete_post'):
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
def choose_group(request, thread_id):
    thread_object = get_object_or_404(Thread, pk=thread_id)

    if thread_object.use_group_logic:

        if not UserGroup.objects.filter(group__thread_id=thread_id, user_id=request.user).exists():

            groups = Group.objects.filter(thread_id=thread_id).order_by('id')

            if groups.count() == 0 or \
                    groups.count() > 0 and groups.last().usergroup_set.count() > 0:
                group = Group()
                group.thread_id = thread_id
                group.save()

                groups = Group.objects.filter(thread_id=thread_id).order_by('id')

            return render(request, 'diskurs/thread/choose_group.html', {'groups': groups, 'thread': thread_object})

        return redirect('diskurs:thread', thread_id=thread_id)

    else:
        return redirect('diskurs:thread', thread_id=thread_id)


@login_required
@transaction.atomic
def choose_group_set(request, thread_id, group_id):
    group_object = get_object_or_404(Group, pk=group_id)

    if group_object.thread.use_group_logic and group_object.thread_id == int(thread_id):

        if group_object.size < group_object.thread.members_in_group:

            if not UserGroup.objects.filter(group__thread_id=thread_id, user_id=request.user.id).exists():
                user_group = UserGroup()
                user_group.group_id = group_id
                user_group.user_id = request.user.id
                user_group.save()

            return redirect('diskurs:thread', thread_id=thread_id)

        return redirect('diskurs:choose_group', thread_id=thread_id)

    return redirect('diskurs:thread', thread_id=thread_id)
