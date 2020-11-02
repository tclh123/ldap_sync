import logging

import ldap

logger = logging.getLogger(__name__)

LDAP_USER_CLASS = [
    'inetOrgPerson',
    'organizationalPerson',
    'person',
    'top',
    'uidObject'
]


class LDAP:
    """
    We use the following schema for users. We can make this configurable in the future releases.

    	name = "givenName"
    	surname = "sn"
    	username = "cn"  # RDN, same as uid
        display_name = "displayName"  # this LDAP attribute can be made up from givenName joined to SN.
		member_of = "memberOf"
		email =  "mail"
        password = "userPassword"
    """
    def __init__(self, ldap_url, people_dn, bind_dn, password):
        self.people_dn = people_dn
        self.l = ldap.initialize(ldap_url)
        self.l.simple_bind_s(bind_dn, password)

    def add_user(self, user):
        logger.info('Ldap.add_user(%s)', user)
        return
        user.generate_password()

        dn = f'cn={user.username},{self.people_dn}'
        record = {
            'objectClass': LDAP_USER_CLASS,
            'givenName': [user.firstname],
            'sn': [user.lastname],
            'uid': [user.username],
            'displayName': [user.display_name],
            'title': [user.title],
            'mail': [user.email],
            'userPassword': [user.password],
        }

        self.l.add_s(dn, ldap.modlist.addModlist(record))
