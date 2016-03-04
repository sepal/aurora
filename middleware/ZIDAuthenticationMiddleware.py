from datetime import datetime
from hashlib import sha1
from hmac import new as hmac_new
from django.conf import settings
from AuroraUser.models import AuroraUser

import logging
logger = logging.getLogger("ZidSSOBackend")


class ZIDAuthenticationMiddleware(object):
    """
    This class is used as the AuthenticationMiddleware on the production server
    """
    def authenticate(self, params):

        param_keys = params.keys()

        if 'sKey' in param_keys:
            hmac_received = params['sKey']
        elif 'logout' in param_keys:
            hmac_received = params['logout']
        else:
            logger.error("Missing parameters for authentication. Abort.")
            return None

        # make sure order is correct by creating a new list and putting in the available keys one by one
        values = ''
        for key in ['oid', 'mn', 'firstName', 'lastName', 'mail']:
            if key in param_keys:
                values += params[key]

        shared_secret = settings.SSO_SHARED_SECRET.encode(encoding='latin1')
        utc_now = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
        now = int(utc_now / 10)
        user = None
        for offset in [0, -1, 1, -2, 2]:
            values_string = values + str(now + offset)
            values_string = values_string.encode(encoding='latin1')
            hmac_calced = hmac_new(shared_secret, values_string, sha1).hexdigest()

            if hmac_calced == hmac_received:
                logger.info("Matching HMAC")
                try:
                    user = AuroraUser.objects.get(matriculation_number=params['mn'])
                except AuroraUser.DoesNotExist:
                    logger.warn("User with Matr.Nr.: %s not found" % params['mn'])
                    try:
                        user = AuroraUser.objects.get(oid=params['oid'])
                    except AuroraUser.DoesNotExist:
                        logger.error("User with OID:%s not found" % params['oid'])
                        user = None

        if user is None:
            logger.error("HMAC doesn't match. Abort.")

        return user

    def get_user(self, user_id):
        try:
            user = AuroraUser.objects.get(pk=user_id)
        except AuroraUser.DoesNotExist:
            user = None

        return user

    def __str__(self):
        return('ZidSSOBackend')

    def __unicode__(self):
        return('ZidSSOBackend')