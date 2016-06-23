import json
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
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
    issues = list(map(lambda issue: {'id': issue.pk, 'title': issue.title, 'lane': issue.lane.id, 'type': issue.type}, issues))

    return render(
        request, 'Feedback/index.html',
        {
            'course': course,
            'lanes': json.dumps(lanes),
            'issues': json.dumps(issues)
        }
    )
