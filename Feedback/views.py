import json
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from Course.models import Course
from .models import Lane, Issue


@login_required
def index(request, course_short_title):
    """index renders a simple html page and adds the react frontend code."""

    # Pass some values directly as js variables, so that the client doesn't
    # has to make additional requests.
    course = Course.get_or_raise_404(course_short_title)
    lanes = Lane.objects.all().filter(hidden=False).order_by('order')
    lanes = list(map(lambda lane: {'id': lane.pk, 'name': lane.name}, lanes))

    issues = Issue.objects.all().only('title', 'lane', 'type', 'title')
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
def issue(request, course_short_title, issue_id):
    return index(request, course_short_title)

@login_required
def api_issue(request, course_short_title, issue_id):
    issue = Issue.objects.get(pk=issue_id)

    return JsonResponse(issue.serializable)
