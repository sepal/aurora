from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from AuroraUser.models import AuroraUser

"""
Custom authentication backend to just pass the AuroraUser
instead of the default Django user in request context.
"""

class AuroraAuthenticationBackend(ModelBackend):

    def get_user(self, user_id):
        try:
            return AuroraUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None