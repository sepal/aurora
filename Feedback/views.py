import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template import RequestContext
from Course.models import Course
from .models import Lane, Issue
from django.http import HttpResponseBadRequest, HttpResponseNotFound, \
    HttpResponseForbidden


@login_required
def index(request, course_short_title):
    """index renders a simple html page and adds the react frontend code."""

    # Pass some values directly as js variables, so that the client doesn't
    # has to make additional requests.
    course = Course.get_or_raise_404(course_short_title)
    lanes = None
    if request.user.is_staff:
        lanes = Lane.objects.all().order_by('order')
    else:
        lanes = Lane.objects.filter(hidden=False).order_by('order')

    lanes = list(map(lambda lane: {
        'id': lane.pk, 'name': lane.name, 'issues': []}, lanes))
    issues = Issue.objects.all()

    issue_data = []

    for issue in issues:
        if issue.type != 'security' or issue.author == request.user \
                or request.user.is_staff:
            issue_data.append(issue.serializable)

    data = {
        # 'course': {
        #     'id': course.pk,
        #     'title': course.title,
        # },
        'lanes': lanes,
        'issues': issue_data
    }

    return render(
        request, 'Feedback/index.html',
        {
            'course': course,
            'data': json.dumps(data)
        }
    )


@login_required
def issue_display(request, course_short_title, issue_id):
    """
    Render the issue, but allow to pass a issue_id. React route will actually
    take care of that.
    """
    return index(request, course_short_title)

@login_required
def api_issue(request, course_short_title, issue_id):
    """
    API callback for getting editing a certain issue.
    """
    issue = Issue.objects.get(pk=issue_id)
    if request.method == 'GET':
        # Only the staff and the author are able to see issues of the type
        # security.
        if issue.type != 'security' \
                or issue.author == request.user or request.user.is_staff:
            return JsonResponse(issue.serializable)
        else:
            raise HttpResponseForbidden
    elif request.method == 'PUT':
        # Only staff or the owner are allowed to edit issues.
        if issue.author != request.user and not request.user.is_staff:
            raise HttpResponseForbidden
        data = json.loads(request.body.decode('utf-8'))

        if 'lane' in data and issue.lane.pk != data['lane']:
            # Only staff is allowed change the issues lane.
            if not request.user.is_staff:
                raise HttpResponseForbidden
            new_lane = Lane.objects.get(pk=data['lane'])
            issue.lane = new_lane

        issue.type = data['type']
        issue.title = data['title']

        if 'body' in data:
            issue.body = data['body']

        issue.save()
        return JsonResponse(issue.serializable)

    return JsonResponse([])


@login_required
def api_new_issue(request, course_short_title):
    """
    API callback to post a new issue.
    """
    if request.method == 'POST':
        course = Course.get_or_raise_404(course_short_title)
        lanes = Lane.objects.all().filter(hidden=False).order_by('order')

        data = json.loads(request.body.decode('utf-8'))
        user = RequestContext(request)['user']

        if 'title' not in data or 'type' not in data or 'body' not in data:
            raise HttpResponseBadRequest

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

    return JsonResponse([])
