import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template import RequestContext
from Course.models import Course
from .models import Lane, Issue
from django.http import HttpResponseBadRequest, HttpResponseNotFound


@login_required
def index(request, course_short_title):
    """index renders a simple html page and adds the react frontend code."""

    # Pass some values directly as js variables, so that the client doesn't
    # has to make additional requests.
    course = Course.get_or_raise_404(course_short_title)
    lanes = Lane.objects.all().filter(hidden=False).order_by('order')
    lanes = list(map(lambda lane: {'id': lane.pk, 'name': lane.name}, lanes))

    issues = Issue.objects.all()
    issues = list(map(lambda issue: issue.serializable_teaser, issues))

    data = {
        'course': {
            'id': course.pk,
            'title': course.title,
        },
        'lanes': lanes,
        'issues': issues
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
    return index(request, course_short_title)


@login_required
def issue_edit(request, course_short_title, issue_id):
    return index(request, course_short_title)


@login_required
def api_issue(request, course_short_title, issue_id):
    issue = Issue.objects.get(pk=issue_id)
    if request.method == 'GET':
        return JsonResponse(issue.serializable)
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))

        if issue.lane.pk != data['lane']:
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
    if request.method == 'POST':
        course = Course.get_or_raise_404(course_short_title)
        # todo: add special check for the security type.
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
