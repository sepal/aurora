from django.shortcuts import render

from .models import Slide


def slides(request, course_short_title=None):

    qs = Slide.objects.all()
    context = {
        "qs": qs,
    }
    return render(request, "slides.html", context)