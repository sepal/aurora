from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Course.models import Course
from django.http import HttpResponseRedirect

@login_required
def index(request, course_short_title):
    course = Course.get_or_raise_404(course_short_title)
    return render(request, 'Feedback/index.html', {'course': course})
