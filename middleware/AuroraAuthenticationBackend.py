from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from AuroraUser.models import AuroraUser

"""
Custom authentication backend to just pass the AuroraUser
instead of the default Django user in request context.
"""

class AuroraAuthenticationBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = AuroraUser
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = AuroraUser.objects.get(matriculation_number=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)

    def get_user(self, user_id):
        try:
            return AuroraUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None