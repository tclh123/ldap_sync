import logging

import ldap
import ldap.modlist

from ldap_sync.user import User

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
        employee_id = employeeNumber  # unique id that can map user in the HR system
        display_name = "displayName"  # this LDAP attribute can be made up from givenName joined to SN.
		member_of = "memberOf"
		email =  "mail"
        password = "userPassword"
    """
    def __init__(self, ldap_url, people_dn, bind_dn, password):
        self.people_dn = people_dn
        self.l = ldap.initialize(ldap_url)
        self.l.simple_bind_s(bind_dn, password)

    def search(self, dn, attr, value='*'):
        search_filter = '(%s=%s)' % (attr, value)
        ret = self.l.search_s(dn, ldap.SCOPE_SUBTREE, search_filter)
        return ret

    def get_user(self, username):
        ret = self.search(self.people_dn, 'cn', username)
        if not ret:
            return None
        dn, record = ret[0]
        # bytes to string
        record = record_convert_bytes(record)
        record = {k: v[0] for k, v in record.items() if v}
        user = User(id=record.get('employeeNumber'),
                    username=record['cn'],
                    firstname=record['givenName'],
                    lastname=record['sn'],
                    display_name=record['displayName'],
                    email=record['mail'],
                    title=record['title'],
                )
        return user

    def add_user(self, user: User):
        logger.info('Ldap.add_user(%s)', user)

        exist_user = self.get_user(user.username)
        if exist_user:
            # the same user, don't add
            if exist_user == user:
                return
            # pick another username to solve conflict
            logger.info('Pick another username for %s, exist %s', user, exist_user)
            for another_name in (user.firstname,
                                 user.firstname + user.lastname[0],
                                 user.firstname + user.lastname):
                another_name = another_name.lower()
                exist_user = self.get_user(another_name)
                if exist_user and exist_user == user:
                    return
                if not exist_user:
                    user.username = another_name
                    break

        # TODO: output, email this password out
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
            'employeeNumber': [user.id],
            'userPassword': [user.password],
        }
        logger.info('ldap add %s, record: %s', dn, record)
        # all attribute values must be list of bytes
        self.l.add_s(dn, ldap.modlist.addModlist(record_convert_bytes(record)))


def record_convert_bytes(record):
    """deal with bytes and text"""
    def f(i):
        if isinstance(i, str):
            return i.encode('utf-8')
        if isinstance(i, bytes):
            return i.decode('utf-8')
        return i
    return {k: [f(i) for i in v] for k, v in record.items()}
