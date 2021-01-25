import json
from typing import Union

from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from common.testing.builders import UserBuilder
from common.testing.testcase_mixins import AuthenticableTestMixin


class TokenCaseMixin(TestCase):

    def assert_access_token(self, access_token):
        self.assertIsInstance(access_token, str)
        self.assertEqual(len(access_token), 205)
        self.assertEqual(len(access_token.split('.')), 3)


class UserViewSetTest(AuthenticableTestMixin):

    def setUp(self) -> None:
        self.client = APIClient()

    def assert_response_user(self, expected: Union[dict, User], actual: dict):
        if isinstance(expected, User):
            self.assertEqual(expected.first_name, actual['firstName'])
            self.assertEqual(expected.last_name, actual['lastName'])
            self.assertEqual(expected.username, actual['username'])
            self.assertEqual(expected.email, actual['email'])
        elif isinstance(expected, dict):
            self.assertEqual(expected['firstName'], actual['firstName'])
            self.assertEqual(expected['lastName'], actual['lastName'])
            self.assertEqual(expected['username'], actual['username'])
            self.assertEqual(expected['email'], actual['email'])
        else:
            ValueError('expected should be an instance de user or dict')

    def assert_persisted_user(self, expected: dict, actual: User):
        self.assertEqual(expected['firstName'], actual.first_name)
        self.assertEqual(expected['lastName'], actual.last_name)
        self.assertEqual(expected['username'], actual.username)
        self.assertEqual(expected['email'], actual.email)
        self.assertEqual(78, len(actual.password))
        self.assertTrue(is_password_usable(actual.password))

    def test_should_register_new_user(self):
        user_data = UserBuilder().with_username('breno')\
                                 .with_password('123456')\
                                 .with_first_name('Breno')\
                                 .with_last_name('Magro')\
                                 .with_email('breno@breno.com')\
                                 .build(json=True)
        url = reverse('user-list')

        response = self.client.post(url, user_data, format='json')
        response_json = json.loads(response.rendered_content.decode())

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assert_response_user(user_data, response_json)
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
        self.authenticate_user(user, '123456')

        response = self.client.get(url, format='json')
        response_json = json.loads(response.rendered_content.decode())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assert_response_user(user, response_json)

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
        self.authenticate_user(user, '123456')
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
