from typing import Union

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class UserBuilder:

    def __init__(self):
        self.user = User()

    def build(self, json=False) -> Union[User, dict]:
        if json:
            return self._as_json()
        return self.user

    def with_username(self, username: str) -> 'UserBuilder':
        self.user.username = username
        return self

    def with_first_name(self, first_name: str) -> 'UserBuilder':
        self.user.first_name = first_name
        return self

    def with_last_name(self, last_name: str) -> 'UserBuilder':
        self.user.last_name = last_name
        return self

    def with_email(self, email: str) -> 'UserBuilder':
        self.user.email = email
        return self

    def with_password(self, password: str) -> 'UserBuilder':
        self.user.password = make_password(password)
        return self

    def _as_json(self) -> dict:
        return {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'password': self.user.password
        }
