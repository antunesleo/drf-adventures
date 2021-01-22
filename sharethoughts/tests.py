
# Create your tests here.
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from sharethoughts.models import Thought


def create_thought(thought: str) -> Thought:
    return Thought(thought=thought)


class ThoughtsListViewTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_should_publish_a_thought(self):
        data = {'thought': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in lectus vitae elit congue interdum sed ut quam. Vivamus at lectus lacus. Proin fringilla porta sapien, vel scelerisque quam aliquet at. Integer faucibus justo nibh, sodales placerat eros consectetur sed. Praesent ultrices felis arcu, at luctus turpis auctor fermentum. '''}
        response = self.client.post(reverse('thoughts-list'), data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Thought.objects.count())
        thought = Thought.objects.get()
        self.assertEqual(data['thought'], thought.thought)
