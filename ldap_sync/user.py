from typing import Optional
from dataclasses import dataclass

from ldap_sync.consts import RANDOM_PASSWORD_LENGTH
from ldap_sync.utils import generate_random_string


@dataclass
class User:
    id: str
    username: str
    firstname: str
    lastname: str
    display_name: str
    email: str
    title: str
    password: Optional[str] = None

    def generate_password(self, length=RANDOM_PASSWORD_LENGTH):
        self.password = generate_random_string(length)

    def __eq__(self, other):
        # consider this as the same user
        return self.id == other.id

    def same_name(self, other):
        return all(getattr(other, attr) == getattr(self, attr)
               for attr in ['firstname', 'lastname', 'username'])
