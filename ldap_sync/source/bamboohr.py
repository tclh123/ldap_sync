import logging

import requests

from ldap_sync.user import User

logger = logging.getLogger(__name__)

EMPLOYEE_API_URL_PATTERN = 'https://api.bamboohr.com/api/gateway.php/{company_domain}/v1/employees/directory'


class BambooHR:
    def __init__(self, config):
        self.config = config

    def get_user_data(self):
        """API reference https://documentation.bamboohr.com/reference"""

        r = requests.get(EMPLOYEE_API_URL_PATTERN.format(company_domain=self.config.bamboohr.company_domain),
                         headers={'Accept': 'application/json'},
                         auth=(self.config.bamboohr.apikey, 'x'))
        r.raise_for_status()
        employees = r.json().get('employees', [])

        for employee in employees:
            username = (employee.get('preferredName', '') or '').lower() or (employee.get('firstName', '') or '').lower()
            email = (employee.get('workEmail') or
                     '%s.%s@%s' % (employee.get('firstName').lower(),
                                   employee.get('lastName').lower(),
                                   self.config.bamboohr.company_email_domain))
            user = User(username=username,
                        firstname=employee.get('firstName'),
                        lastname=employee.get('lastName'),
                        email=email,
                        title=employee.get('jobTitle'),
                    )

            yield user
