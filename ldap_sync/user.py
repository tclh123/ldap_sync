from typing import Optional
from random import sample
from dataclasses import dataclass

from ldap_sync.consts import RANDOM_PASSWORD_LENGTH

@dataclass
class User:
    username: str
    firstname: str
    lastname: str
    email: str
    title: str
    password: Optional[str] = None

    def generate_password(self, length=RANDOM_PASSWORD_LENGTH):
        seed = '23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
        self.password = ''.join(sample(seed, length))
