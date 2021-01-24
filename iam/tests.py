from copy import deepcopy
from typing import Union

from django.contrib.auth.hashers import make_password, is_password_usable
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from rest_framework.reverse import reverse
from rest_framework.test import APIClient


USERS_DATASET = [
    {
        'first_name': 'Breno',
        'last_name': 'Magro',
        'username': 'breno',
        'email': 'breno@breno.com',
        'password': '123456'
    },
    {
        'first_name': 'Adagalmir',
        'last_name': 'Silva',
        'username': 'agaga',
        'email': 'adaga@adaga.com',
        'password': '123456'
    }
]


def get_test_user(index: int) -> dict:
    return deepcopy(USERS_DATASET[index])


def create_user(user_data: dict) -> User:
    user_data = deepcopy(user_data)
    password = user_data.pop('password')
    user = User(**user_data)
    user.password = make_password(password)
    user.save()
    return user


def assert_access_token(testcase, access_token):
    testcase.assertIsInstance(access_token, str)
    testcase.assertEqual(len(access_token), 205)
    testcase.assertEqual(len(access_token.split('.')), 3)


class UserViewSetTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def assert_response_user(self, expected: dict, actual: dict):
        self.assertEqual(expected['first_name'], actual['first_name'])
        self.assertEqual(expected['last_name'], actual['last_name'])
        self.assertEqual(expected['username'], actual['username'])
        self.assertEqual(expected['email'], actual['email'])

    def assert_persisted_user(self, expected: dict, actual: User):
        self.assertEqual(expected['first_name'], actual.first_name)
        self.assertEqual(expected['last_name'], actual.last_name)
        self.assertEqual(expected['username'], actual.username)
        self.assertEqual(expected['email'], actual.email)
        self.assertEqual(78, len(actual.password))
        self.assertTrue(is_password_usable(actual.password))

    def test_should_register_new_user(self):
        user_data = get_test_user(0)
        url = reverse('user-list')

        response = self.client.post(url, user_data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assert_response_user(user_data, response.data)
        persisted_user = User.objects.get()
        self.assert_persisted_user(user_data, persisted_user)

    # TODO: Use user dataset
    def test_should_not_register_a_new_user_if_username_in_use(self):
        user_data = {
            'first_name': 'Breno',
            'last_name': 'Brenudo',
            'username': 'breno',
            'email': 'breno@breno.com',
            'password': '123456'
        }
        create_user(user_data)
        url = reverse('user-list')
        user_data = {
            'first_name': 'Breno',
            'last_name': 'Brenudo',
            'username': 'breno',
            'email': 'breno2@breno.com',
            'password': '123456'
        }

        response = self.client.post(url, user_data, format='json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_should_not_register_a_new_user_if_email_in_use(self):
        first_user_data = get_test_user(0)
        second_user_data = get_test_user(1)
        second_user_data['email'] = first_user_data['email']
        create_user(first_user_data)

        url = reverse('user-list')
        response = self.client.post(url, second_user_data, format='json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class TokenObtainPairViewTest(TestCase):

    def assert_refresh_token(self, refresh_token):
        self.assertIsInstance(refresh_token, str)
        self.assertEqual(len(refresh_token), 207)
        self.assertEqual(len(refresh_token.split('.')), 3)

    def test_should_obtain_pair_token(self):
        user_data = get_test_user(0)
        create_user(user_data)
        url = reverse('token_obtain_pair')

        credentials = {
            'username': user_data['username'],
            'password': user_data['password']
        }
        response = self.client.post(url, credentials, format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assert_refresh_token(response.data['refresh'])
        assert_access_token(self, response.data['access'])

    def test_should_not_obtain_token_if_wrong_credentials(self):
        user_data = get_test_user(0)
        create_user(user_data)

        credentials = {
            'username': user_data['username'],
            'password': 'wrong password'
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, credentials, format='json')

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class TokenRefreshViewTest(TestCase):

    def test_should_refresh_token(self):
        user_data = get_test_user(0)
        create_user(user_data)
        credentials = {
            'username': user_data['username'],
            'password': user_data['password']
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, credentials, format='json')

        payload = {
            'refresh': response.data['refresh']
        }
        url = reverse('token_refresh')
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_access_token(self, response.data['access'])

    def test_should_not_refresh_when_token_is_invalid_or_expired(self):
        payload = {
            'refresh': 'fadsfsdafsadfsadf'
        }
        url = reverse('token_refresh')
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
