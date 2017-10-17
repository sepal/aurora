from django.core import urlresolvers
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from AuroraProject.decorators import aurora_login_required
from Notification.models import Notification, FeedToken
from AuroraUser.models import AuroraUser
from Course.models import Course, CourseUserRelation


@aurora_login_required()
def notifications(request, course_short_title=None):
    data = {}
    user = request.user
    course = Course.get_or_raise_404(course_short_title)

    # check if rss token was already generated, if not generate it
    FeedToken.get_or_create_token(user)

    if 'id' in request.GET:
        try:
            notification = Notification.objects.get(pk=request.GET['id'])
            if not notification.user == user:
                raise Http404
        except:
            raise Http404

        notification.read = True
        notification.save()

        if 'link' in request.GET:
            return redirect(request.GET['link'])

        return redirect('Notification:list', course_short_title=course_short_title)
    notifications = Notification.objects.filter(user=user, course=course).order_by('-creation_time')
    data['notifications'] = notifications
    data['course'] = course

    try:
        data['feed_token'] = FeedToken.objects.get(user=request.user)
    except FeedToken.DoesNotExist:
        data['feed_token'] = None

    return render(request, 'notifications.html', data)


@aurora_login_required()
@staff_member_required
def write_notification(request, course_short_title=None):
    if not 'user' in request.GET:
        raise Http404
    data = {
        'user_id': request.GET['user'],
        'course_short_title': course_short_title,
    }
    return render(request, 'send_notification.html', data)


@aurora_login_required()
@staff_member_required
def send_notification(request, course_short_title=None):
    if not 'user_id' in request.POST:
        raise Http404
    if not 'message' in request.POST:
        raise Http404
    user = AuroraUser.objects.get(pk=request.POST['user_id'])
    text = request.POST['message']
    link = ""
    if 'link' in request.POST:
        link = request.POST['link']
    course_ids = CourseUserRelation.objects.filter(user=user).values_list('course', flat=True)
    courses = Course.objects.filter(id__in=course_ids)
    for course in courses:
        obj, created = Notification.objects.get_or_create(
            user=user,
            course=course,
            text=text,
            link=link
        )
    return HttpResponse("Notification sent to user with id: %s" % user.nickname)


@aurora_login_required()
def read(request, course_short_title=None):
    user = request.user
    course = Course.get_or_raise_404(course_short_title)
    notifications = Notification.objects.filter(user=user, course=course)
    for notification in notifications:
        if not notification.user == user:
            raise Http404
        notification.read = True
        notification.save()
    return HttpResponse()


@aurora_login_required()
def refresh(request, course_short_title=None):
    user = request.user
    course = Course.get_or_raise_404(course_short_title)
    notifications = Notification.objects.filter(user=user, course=course, read=False)
    return HttpResponse(len(notifications))


