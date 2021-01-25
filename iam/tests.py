from typing import Union

from django.contrib.auth.hashers import make_password, is_password_usable
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from rest_framework.reverse import reverse
from rest_framework.test import APIClient


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


class TokenCaseMixin(TestCase):

    def assert_access_token(self, access_token):
        self.assertIsInstance(access_token, str)
        self.assertEqual(len(access_token), 205)
        self.assertEqual(len(access_token.split('.')), 3)


class UserViewSetTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def assert_response_user(self, expected: Union[dict, User], actual: dict):
        if isinstance(expected, User):
            self.assertEqual(expected.first_name, actual['first_name'])
            self.assertEqual(expected.last_name, actual['last_name'])
            self.assertEqual(expected.username, actual['username'])
            self.assertEqual(expected.email, actual['email'])
        elif isinstance(expected, dict):
            self.assertEqual(expected['first_name'], actual['first_name'])
            self.assertEqual(expected['last_name'], actual['last_name'])
            self.assertEqual(expected['username'], actual['username'])
            self.assertEqual(expected['email'], actual['email'])
        else:
            ValueError('expected should be an instance de user or dict')

    def assert_persisted_user(self, expected: dict, actual: User):
        self.assertEqual(expected['first_name'], actual.first_name)
        self.assertEqual(expected['last_name'], actual.last_name)
        self.assertEqual(expected['username'], actual.username)
        self.assertEqual(expected['email'], actual.email)
        self.assertEqual(78, len(actual.password))
        self.assertTrue(is_password_usable(actual.password))

    def obtain_and_configure_access_token(self, username: str, password: str):
        url = reverse('token_obtain_pair')
        response = self.client.post(
            url,
            {'username': username, 'password': password},
            format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_should_register_new_user(self):
        user_data = UserBuilder().with_username('breno')\
                                 .with_password('123456')\
                                 .with_first_name('Breno')\
                                 .with_last_name('Magro')\
                                 .with_email('breno@breno.com')\
                                 .build(json=True)
        url = reverse('user-list')

        response = self.client.post(url, user_data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assert_response_user(user_data, response.data)
        persisted_user = User.objects.get()
        self.assert_persisted_user(user_data, persisted_user)

    def test_should_not_register_a_new_user_if_username_in_use(self):
        first_user = UserBuilder().with_username('breno')\
                                  .with_password('123456')\
                                  .with_first_name('Breno')\
                                  .with_last_name('Magro')\
                                  .with_email('breno@breno.com')\
                                  .build()
        first_user.save()
        second_user_data = UserBuilder().with_username('breno')\
                                        .with_password('123456')\
                                        .with_first_name('Breno2')\
                                        .with_last_name('Magro2')\
                                        .with_email('breno@breno.com')\
                                        .build(json=True)
        url = reverse('user-list')

        response = self.client.post(url, second_user_data, format='json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_should_not_register_a_new_user_if_email_in_use(self):
        first_user = UserBuilder().with_username('breno')\
                                  .with_password('123456')\
                                  .with_first_name('Breno')\
                                  .with_last_name('Magro')\
                                  .with_email('breno@breno.com')\
                                  .build()
        first_user.save()
        second_user_data = UserBuilder().with_username('breno2')\
                                        .with_password('123456')\
                                        .with_first_name('Breno2')\
                                        .with_last_name('Magro2')\
                                        .with_email('breno@breno.com')\
                                        .build(json=True)

        url = reverse('user-list')
        response = self.client.post(url, second_user_data, format='json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_should_get_user_info(self):
        user = UserBuilder().with_username('breno')\
                            .with_password('123456')\
                            .with_first_name('Breno')\
                            .with_last_name('Magro')\
                            .with_email('breno@breno.com')\
                            .build()
        user.save()
        url = reverse('user-detail', kwargs={'pk': user.id})
        self.obtain_and_configure_access_token(user.username, '123456')

        response = self.client.get(url, format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assert_response_user(user, response.data)

    def test_should_not_get_user_info_when_not_authenticated(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_authenticated_user_should_not_see_info_from_another_user(self):
        user = UserBuilder().with_username('breno')\
                            .with_password('123456')\
                            .with_first_name('Breno')\
                            .with_last_name('Magro')\
                            .with_email('breno@breno.com')\
                            .build()
        user.save()
        self.obtain_and_configure_access_token(user.username, '123456')
        other_user = UserBuilder().with_username('breno2')\
                                  .with_password('123456')\
                                  .with_first_name('Breno2')\
                                  .with_last_name('Magro2')\
                                  .with_email('breno2@breno.com')\
                                  .build()
        other_user.save()

        url = reverse('user-detail', kwargs={'pk': other_user.id})
        response = self.client.get(url, format='json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class TokenCaseObtainPairViewTest(TokenCaseMixin):

    def assert_refresh_token(self, refresh_token):
        self.assertIsInstance(refresh_token, str)
        self.assertEqual(len(refresh_token), 207)
        self.assertEqual(len(refresh_token.split('.')), 3)

    def test_should_obtain_pair_token(self):
        user = UserBuilder().with_username('breno')\
                            .with_password('123456')\
                            .with_first_name('Breno')\
                            .with_last_name('Magro')\
                            .with_email('breno@breno.com')\
                            .build()
        user.save()

        url = reverse('token_obtain_pair')
        credentials = {
            'username': 'breno',
            'password': '123456'
        }
        response = self.client.post(url, credentials, format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assert_refresh_token(response.data['refresh'])
        self.assert_access_token(response.data['access'])

    def test_should_not_obtain_token_if_wrong_credentials(self):
        user = UserBuilder().with_username('breno')\
                            .with_password('123456')\
                            .with_first_name('Breno')\
                            .with_last_name('Magro')\
                            .with_email('breno@breno.com')\
                            .build()
        user.save()

        credentials = {
            'username': 'breno',
            'password': 'wrong password'
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, credentials, format='json')

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class TokenCaseRefreshViewTest(TokenCaseMixin):

    def test_should_refresh_token(self):
        user = UserBuilder().with_username('breno')\
                            .with_password('123456')\
                            .with_first_name('Breno')\
                            .with_last_name('Magro')\
                            .with_email('breno@breno.com')\
                            .build()
        user.save()
        credentials = {
            'username': 'breno',
            'password': '123456'
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, credentials, format='json')

        payload = {'refresh': response.data['refresh']}
        url = reverse('token_refresh')
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_access_token(response.data['access'])

    def test_should_not_refresh_when_token_is_invalid_or_expired(self):
        url = reverse('token_refresh')
        data = {'refresh': 'fadsfsdafsadfsadf'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
