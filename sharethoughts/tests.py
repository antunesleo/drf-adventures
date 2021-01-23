
# Create your tests here.
from datetime import datetime
from typing import Union

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from sharethoughts.models import Thought


def create_thought(thought: str) -> Thought:
    thought = Thought(thought=thought)
    thought.save()
    return thought


class ThoughtViewSetTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        user_data = {
            'first_name': 'Breno',
            'last_name': 'Magro',
            'username': 'breno',
            'email': 'breno@breno.com',
            'password': '123456'
        }
        url = reverse('user-list')
        response = self.client.post(url, user_data, format='json')
        self.auth_user = response.data

    def obtain_and_configure_access_token(self):
        credentials = {
            'username': self.auth_user['username'],
            'password': '123456'
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, credentials, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def assert_thought(
      self,
      expected_thought: str,
      actual_thought: Union[Thought, dict]
    ):
        if isinstance(actual_thought, dict):
            self.assertEqual(expected_thought, actual_thought['thought'])
            self.assertEqual(
                datetime.today().strftime('%Y-%m-%d'),
                actual_thought['created_at'][0:10],
            )
        elif isinstance(actual_thought, Thought):
            self.assertEqual(expected_thought, actual_thought.thought)
            self.assertEqual(
                datetime.today().strftime('%Y-%m-%d'),
                actual_thought.created_at.strftime('%Y-%m-%d'),
            )
        else:
            raise TypeError('atual_thought must be instance of Thought or dict')

    def test_should_publish_a_thought(self):
        self.obtain_and_configure_access_token()
        data = {'thought': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in lectus vitae elit congue interdum sed ut quam. Vivamus at lectus lacus. Proin fringilla porta sapien, vel scelerisque quam aliquet at. Integer faucibus justo nibh, sodales placerat eros consectetur sed. Praesent ultrices felis arcu, at luctus turpis auctor fermentum.'''}
        url = reverse('thought-list')
        self.client.request()
        response = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Thought.objects.count())
        thought = Thought.objects.get()
        self.assert_thought(data['thought'], thought)

    def test_should_no_publish_a_thought_bigger_than_800_characters(self):
        self.obtain_and_configure_access_token()
        data = {'thought': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in lectus vitae elit congue interdum sed ut quam. Vivamus at lectus lacus. Proin fringilla porta sapien, vel scelerisque quam aliquet at. Integer faucibus justo nibh, sodales placerat eros consectetur sed. Praesent ultrices felis arcu, at luctus turpis auctor fermentum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in lectus vitae elit congue interdum sed ut quam. Vivamus at lectus lacus. Proin fringilla porta sapien, vel scelerisque quam aliquet at. Integer faucibus justo nibh, sodales placerat eros consectetur sed. Praesent ultrices felis arcu, at luctus turpis auctor fermentum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in lectus vitae elit congue interdum sed ut quam. Vivamus at lectus lacus. Proin fringilla porta sapien, vel scelerisque quam aliquet at. Integer faucibus justo nibh, sodales placerat eros consectetur sed. Praesent ultrices felis arcu, at luctus turpis auctor fermentum.'}
        url = reverse('thought-list')

        response = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, Thought.objects.count())

    def test_should_list_all_thoughts(self):
        create_thought('Lorem ipsum dolor sit amet')
        create_thought('consectetur adipiscing elit.')

        url = reverse('thought-list')

        response = self.client.get(url, format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assert_thought('Lorem ipsum dolor sit amet', response.data[0])
        self.assert_thought('consectetur adipiscing elit.', response.data[1])
