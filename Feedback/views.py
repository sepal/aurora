import json
from django.shortcuts import render
from AuroraProject.decorators import aurora_login_required
from django.http import JsonResponse
from django.template import RequestContext
from Course.models import Course
from .models import Lane, Issue, Upvote
from django.http import HttpResponseBadRequest, HttpResponseNotFound, \
    HttpResponseForbidden
from django.views.decorators.http import require_http_methods


@aurora_login_required()
def index(request, course_short_title):
    """
    index renders a simple html page, adds the react frontend code and some
    initial data, so that users don't have to make additional request to see
    the issues.
    """

    # Pass some values directly as js variables, so that the client doesn't
    # has to make additional requests.
    course = Course.get_or_raise_404(course_short_title)

    lanes = None
    if request.user.is_staff:
        lanes = Lane.objects.all().order_by('order')
    else:
        # Only staff is allowed to see hidden lanes.
        lanes = Lane.objects.filter(hidden=False).order_by('order')

    lanes = list(map(lambda lane: {
        'id': lane.pk, 'name': lane.name, 'issues': []}, lanes))

    # Issues are course specific.
    issues = Issue.objects.filter(course=course)
    upvotes = Upvote.objects.filter(user=request.user)

    issue_data = []
    for issue in issues:
        # Filter out any security issues, if the current user is not the owner
        # or an admin.
        if issue.type != 'security' or issue.author == request.user \
                or request.user.is_staff:
            data = issue.serializable
            data['upvoted'] = issue.upvoted(request.user)
            issue_data.append(data)

    data = {
        'lanes': lanes,
        'issues': issue_data,
        'current_user': {
            'is_staff': request.user.is_staff,
            'id': request.user.id,
        }
    }

    return render(
        request, 'Feedback/index.html',
        {
            'course': course,
            'data': json.dumps(data)
        }
    )


@aurora_login_required()
def issue_display(request, course_short_title, issue_id):
    """
    Basically the same as the index, since react route will take care of
    showing the specific issue. Couldn't find out how to move all into the
    index function otherwise.
    """
    return index(request, course_short_title)


@aurora_login_required()
@require_http_methods(['PUT'])
def api_issue(request, course_short_title, issue_id):
    """
    API callback for editing g a certain issue.
    """
    issue = Issue.objects.get(pk=issue_id)

    # Only staff or the owner are allowed to edit issues.
    if issue.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden()

    # Decoded the passed values.
    data = json.loads(request.body.decode('utf-8'))

    # Check if the user wants to switch the lane.
    if 'lane' in data and issue.lane.pk != data['lane']:
        # Only staff is allowed to change the issues lane.
        if not request.user.is_staff:
            return HttpResponseForbidden()
        new_lane = Lane.objects.get(pk=data['lane'])
        issue.lane = new_lane

    # Users can only edit the type, title or the body of an issue.
    if 'type' in data:
        issue.type = data['type']

    if 'title' in data:
        issue.title = data['title']

    if 'body' in data:
        issue.body = data['body']

    issue.save()

    # Return the issue, so redux/react can update the kanban immediately.
    return JsonResponse(issue.serializable)


@aurora_login_required()
@require_http_methods(['POST'])
def api_new_issue(request, course_short_title):
    """
    API callback to create a new issue.
    """

    course = Course.get_or_raise_404(course_short_title)
    lanes = Lane.objects.all().filter(hidden=False).order_by('order')

    data = json.loads(request.body.decode('utf-8'))
    user = RequestContext(request)['user']

    # You can't create an issue without a title, type or a body.
    if 'title' not in data or 'type' not in data or 'body' not in data:
        return HttpResponseForbidden()

    issue = Issue(
        author=user,
        course=course,
        lane=lanes[0],
        type=data['type'],
        title=data['title'],
        body=data['body'],
    )

    issue.save()
    return JsonResponse(issue.serializable)


@aurora_login_required()
def issue_comments(request, course_short_title, issue_id):
    """
    Special API callback that returns the html part of the comments for a
    certain issue.
    This is necessary, since the Feedback system reuses the Comments client
    side code.
    """
    issue = Issue.objects.get(pk=issue_id)
    # Only the staff and the author are able to see issues of the type
    # security.
    if issue.type == 'security' \
            and issue.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden()

    context = {
        'issue': issue,
        'course': Course.get_or_raise_404(course_short_title)
    }

    return render(request, "issue_comments.html", context)


@aurora_login_required()
@require_http_methods('POST')
def api_upvote(request, course_short_title, issue_id):
    """
    Registers a new upvote for the given issue.
    """

    issue = Issue.objects.get(pk=issue_id)

    # Only the staff and the author are able to see issues of the type
    # security.
    if issue.type == 'security' \
            and issue.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden()

    # You can only up vote once.
    if Upvote.exists(request.user, issue):
        return HttpResponseForbidden()

    # todo: determine if staff users and owner of the issue can up vote an
    # issue.
    upvote = Upvote(user=request.user, issue=issue)
    upvote.save()

    # Return the number of up votes, so that the client side code can update
    # the number.
    upvotes = Upvote.objects.filter(issue=issue).count()

    response = {
        'issue_id': issue_id,
        'upvotes': upvotes
    }
    return JsonResponse(response)
