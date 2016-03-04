from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from AuroraUser.models import AuroraUser


class DjangoAuthenticationMiddleware(object):
    """
    AuthenticationMiddleware so that request.user is of type AuroraUser.
    """

    def authenticate(self, username=None, password=None):
        try:
            user = AuroraUser.objects.get(username=username)

            if check_password(password, user.password):
                return user

        except AuroraUser.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        try:
            return AuroraUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None