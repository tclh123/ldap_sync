from typing import Optional
from random import sample
from dataclasses import dataclass

from ldap_sync.consts import RANDOM_PASSWORD_LENGTH

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
        seed = '23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
        self.password = ''.join(sample(seed, length))

    def __eq__(self, other):
        # consider this as the same user
        return all(getattr(other, attr) == getattr(self, attr)
               for attr in ['firstname', 'lastname', 'username'])
