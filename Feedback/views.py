from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Course.models import Course

@login_required
def new(request, course_short_title):
    course = Course.get_or_raise_404(course_short_title)
    return render(request, 'Feedback/post.html', {'course': course})