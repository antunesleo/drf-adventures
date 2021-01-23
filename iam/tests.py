from typing import Union

from django.contrib.auth.hashers import make_password, is_password_usable
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class UserViewSetTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        user.save()
        return user

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
        user_data = {
            'first_name': 'Breno',
            'last_name': 'Brenudo',
            'username': 'breno',
            'email': 'breno@breno.com',
            'password': '123456'
        }
        url = reverse('user-list')

        response = self.client.post(url, user_data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assert_response_user(user_data, response.data)
        persisted_user = User.objects.get()
        self.assert_persisted_user(user_data, persisted_user)

    def test_should_not_register_a_new_user_if_username_in_use(self):
        user_data = {
            'first_name': 'Breno',
            'last_name': 'Brenudo',
            'username': 'breno',
            'email': 'breno@breno.com',
            'password': '123456'
        }
        self.create_user(user_data)
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
        user_data = {
            'first_name': 'Breno',
            'last_name': 'Brenudo',
            'username': 'breno',
            'email': 'breno@breno.com',
            'password': '123456'
        }
        self.create_user(user_data)
        url = reverse('user-list')
        user_data = {
            'first_name': 'Breno',
            'last_name': 'Brenudo',
            'username': 'breno2',
            'email': 'breno@breno.com',
            'password': '123456'
        }

        response = self.client.post(url, user_data, format='json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
