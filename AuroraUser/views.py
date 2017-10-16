from django.views.decorators.http import require_GET, require_POST
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as django_login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from AuroraUser.models import AuroraUser
from django.core.urlresolvers import reverse
from Course.models import Course
from django.conf import settings
from Evaluation.views import get_points
from Statistics.views import create_stat_data
from middleware.AuroraAuthenticationBackend import AuroraAuthenticationBackend

from AuroraProject.decorators import aurora_login_required
from Notification.models import FeedToken

import logging
logger = logging.getLogger(__name__)


@require_POST
def signin(request, course_short_title=None):

    if 'username' not in request.POST or 'password' not in request.POST or 'remember' not in request.POST:
        response_data = {'success': False, 'message': 'Something went wrong. Please contact the LVA team'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    if request.POST['remember'] == 'false':
        request.session.set_expiry(0)

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is None:
        response_data = {'success': False, 'message': 'Your username or password was incorrect.'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    if not user.is_active:
        response_data = {'success': False, 'message': 'Your account has been disabled!'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    django_login(request, user)

    # fetch gravatar img on first login
    if not AuroraUser.objects.all().get(id=user.id).avatar:
        AuroraUser.objects.all().get(id=user.id).get_gravatar()

    response_data = {'success': True}
    return HttpResponse(json.dumps(response_data), content_type="application/json")



def signout(request, course_short_title=None):
    logout(request)
    return redirect(reverse('home', args=(course_short_title,)))


@ensure_csrf_cookie
def login(request, course_short_title=None):

    if 'next_url' in request.session and request.session['next_url'] is not None:
        next_url = request.session['next_url']
    else:
        next_url = reverse('home', args=(course_short_title, ))

    sso_uri = settings.SSO_URI.replace("%%NEXT_URL%%", next_url)

    data = {
        'course': Course.get_or_raise_404(course_short_title),
        'signin_url': reverse('User:signin', args=(course_short_title, )),
        'next': next_url,
        'sso_uri': sso_uri
    }

    if 'error_message' in request.GET:
        data.update({'error_message': request.GET['error_message']})
        return render(request, 'login.html', data)
    else:
        return render(request, 'login.html', data)


@require_GET
def sso_auth_callback(request):
    """
    This view is used in conjunction with ZIDAuthenticationMiddleware
    :param request:
    :return:
    """

    values = request.GET

    user = authenticate(params=values)

    if user is None:
        logger.error("User with following params not found")
        logger.error(values)

    if user is None:
        return redirect(reverse('course_selection'))

    if not user.is_active:
        return redirect(reverse('course_selection'))

    django_login(request, user)

    if not user.avatar:
        user.get_gravatar()

    # redirect the user to his/her desired location
    if 'param' in request.GET:
        return HttpResponseRedirect(request.GET.get('param', ""))

    return redirect(reverse('course_selection'))


@aurora_login_required()
@ensure_csrf_cookie
def profile(request, course_short_title):
    user = request.user
    course = Course.get_or_raise_404(course_short_title)

    feed_token = None
    try:
        feed_token = FeedToken.objects.get(user=user)
    except FeedToken.DoesNotExist:
        pass

    context = {
        'user': user,
        'course': course,
        'feed_token': feed_token,
    }

    return render(request, 'profile.html', context)


@aurora_login_required()
def profile_save(request, course_short_title):
    data = {}
    user = request.user
    text_limit = 100
    valid_nickname = True
    if 'nickname' in request.POST and request.POST['nickname'] == "":
        data['error'] = "empty nickname not allowed"
        valid_nickname = False
    nickname_limit = 30
    if len(request.POST['nickname']) > nickname_limit:
        data['error'] = "nickname too long (%s character limit)" % nickname_limit
        valid_nickname = False

    users_with_same_nickname = AuroraUser.objects.filter(nickname=request.POST['nickname']).exclude(id=user.id)
    if len(users_with_same_nickname) > 0:
        data['error'] = "nickname already taken"
        valid_nickname = False

    if valid_nickname:
        user.nickname = request.POST['nickname']

    if is_valid_email(request.POST['email'], text_limit):
        user.email = request.POST['email']
    else:
        data['error'] = "not a valid email address"

    if 'file' in request.FILES:
        user.avatar = request.FILES['file']
    if len(request.POST['study_code']) < text_limit:
        user.study_code = request.POST['study_code']
    else:
        data['error'] = "not a valid study code"
    if len(request.POST['statement']) < text_limit:
        user.statement = request.POST['statement']
    else:
        data['error'] = "statement too long (%s character limit)" % text_limit
    user.save()
    data['nickname'] = user.nickname
    data['email'] = user.email
    data['study_code'] = user.study_code
    data['statement'] = user.statement
    return HttpResponse(json.dumps(data))


def is_valid_email(email, text_limit):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    if len(email) > text_limit:
        return False
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


@aurora_login_required()
@require_GET
def create_feed_token(request, course_short_title):
    feed_token = FeedToken.create_new_token(request.user)

    data = {
        'token': str(feed_token.token)
    }

    return HttpResponse(json.dumps(data), content_type="application/json")

@aurora_login_required()
def work(request, course_short_title):
    user = AuroraAuthenticationBackend.get_user(AuroraAuthenticationBackend(), request.user.id)
    course = Course.get_or_raise_404(course_short_title)

    data = get_points(request, user, course)
    data = create_stat_data(course,data)

    # context = RequestContext(request, data)
    # return render_to_response('work.html', data, context)

    return render(request, 'work.html', data)
