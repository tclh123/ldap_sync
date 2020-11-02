import logging

import requests

from ldap_sync.user import User

logger = logging.getLogger(__name__)

EMPLOYEE_API_URL_PATTERN = 'https://api.bamboohr.com/api/gateway.php/{company_domain}/v1/employees/directory'


class BambooHR:
    def __init__(self, config):
        self.config = config

    def filter(self, employee):
        for f in self.config.bamboohr.filters.split(','):
            attr, value = f.split(':')
            if employee.get(attr) == value:
                return True
        return False

    def get_user_data(self):
        """API reference https://documentation.bamboohr.com/reference"""

        r = requests.get(EMPLOYEE_API_URL_PATTERN.format(company_domain=self.config.bamboohr.company_domain),
                         headers={'Accept': 'application/json'},
                         auth=(self.config.bamboohr.apikey, 'x'))
        r.raise_for_status()
        employees = r.json().get('employees', [])

        for employee in employees:
            if not self.filter(employee):
                continue

            username = (employee.get('preferredName', '') or '').lower() or (employee.get('firstName', '') or '').lower()
            firstname = employee.get('firstName')
            lastname = employee.get('lastName')
            email = (employee.get('workEmail') or
                     '%s.%s@%s' % (firstname.lower(),
                                   lastname.lower(),
                                   self.config.bamboohr.company_email_domain))
            user = User(username=username,
                        firstname=firstname,
                        lastname=lastname,
                        display_name=employee.get('displayName') or f'{firstname} {lastname}',
                        email=email,
                        id=employee.get('id'),
                        title=employee.get('jobTitle'),
                    )

            yield user
