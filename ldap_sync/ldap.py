import logging

logger = logging.getLogger(__name__)


class LDAP:
    def __init__(self, ldap_url):
        pass

    def add_user(self, user):
        logger.info('Ldap.add_user(%s)', user)
        pass
