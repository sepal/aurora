from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.utils.six.moves.urllib.parse import urlparse
from django.shortcuts import resolve_url
from Course.models import Course

def aurora_login_required():
    """
    Decorator for views that checks that the user is authenticated by checking
    if the user has logged in correctly and has the right permissions:

     - Every user has to authenticate using his password
     - A staff user can visit every course
     - A normal user can visit just the course he is enlisted in

     This decorator works just for views for whose url contains the course short title.
     It is then extracted and used to authenticate the user.

    Usage: Put @aurora_login_required() right above a view function. Remember to not forget the brackets.

    TODO: discuss if it would be better to use first view argument as course_short_title
     instead of extracting course_short_title from request path. It would imply that every view
     using the @aurora_login_required() decorator has a course_short_title as first parameter.
    """

    def decorator(view_func):

        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            try:
                course_title = request.path.split("/")[1]
                course = Course.objects.get(short_title=course_title)
            except (IndexError, Course.DoesNotExist):
                assert False, "aurora_login_required - can only be used when the url contains the course."

            if request.user.is_authenticated() and (request.user.is_staff or course.user_is_enlisted(request.user)):
                return view_func(request, *args, **kwargs)

            path = request.build_absolute_uri()
            # urlparse chokes on lazy objects in Python 3, force to str
            resolved_login_url = force_str(
                resolve_url(settings.LOGIN_URL))
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, REDIRECT_FIELD_NAME)
        return _wrapped_view
    return decorator