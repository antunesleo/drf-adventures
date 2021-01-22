
# Create your tests here.
from datetime import datetime
from typing import Union

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from sharethoughts.models import Thought


def create_thought(thought: str) -> Thought:
    thought = Thought(thought=thought)
    thought.save()
    return thought


class ThoughtsListViewTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

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
        data = {'thought': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in lectus vitae elit congue interdum sed ut quam. Vivamus at lectus lacus. Proin fringilla porta sapien, vel scelerisque quam aliquet at. Integer faucibus justo nibh, sodales placerat eros consectetur sed. Praesent ultrices felis arcu, at luctus turpis auctor fermentum.'''}
        url = reverse('thought-list')

        response = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Thought.objects.count())
        thought = Thought.objects.get()
        self.assert_thought(data['thought'], thought)

    def test_should_no_publish_a_thought_bigger_than_800_characters(self):
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
