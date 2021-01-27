from typing import Union

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from common.testing.builders import UserBuilder
from common.testing.testcase_mixins import AuthenticableTestMixin
from sharethoughts.models import Thought


class ThoughtBuilder:

    def __init__(self):
        self.thought = Thought()

    def build(self, json=False) -> Union[Thought, dict]:
        if json:
            return self._as_json()
        return self.thought

    def with_thought(self, thought: str) -> 'ThoughtBuilder':
        self.thought.thought = thought
        return self

    def with_owner(self, owner: User) -> 'ThoughtBuilder':
        self.thought.owner = owner
        return self

    def _as_json(self) -> dict:
        return {
            'thought': self.thought.thought,
            'owner': self.thought.owner.username
        }


class ThoughtCaseMixin(TestCase):

    def assert_response_thought(self, expected: dict, actual: dict):
        self.assertEqual(expected['thought'], actual['thought'])
        self.assertEqual(expected['user']['username'], actual['user']['username'])


class ThoughtViewSetTest(ThoughtCaseMixin, AuthenticableTestMixin):

    def setUp(self) -> None:
        self.client = APIClient()
        super(ThoughtViewSetTest, self).setUp()

    def test_should_publish_a_thought(self):
        user = UserBuilder().with_first_name('Bren') \
                            .with_last_name('Magro') \
                            .with_username('breninho') \
                            .with_email('brenoninho@breno.com') \
                            .with_password('123456') \
                            .build()
        user.save()
        self.authenticate_user(user, '123456')
        data = {'thought': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in lectus vitae elit congue interdum sed ut quam. Vivamus at lectus lacus. Proin fringilla porta sapien, vel scelerisque quam aliquet at. Integer faucibus justo nibh, sodales placerat eros consectetur sed. Praesent ultrices felis arcu, at luctus turpis auctor fermentum.'''}

        url = reverse('thought-list')
        self.client.request()
        response = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Thought.objects.count())
        expected_thought = {
            'thought': data['thought'],
            'user': {'username': user.username}
        }
        self.assert_response_thought(
            expected_thought,
            response.data
        )
        thought = Thought.objects.get()
        self.assertEqual(expected_thought['thought'], thought.thought)
        self.assertEqual(expected_thought['user']['username'], thought.owner.username)

    def test_should_no_publish_a_thought_bigger_than_800_characters(self):
        user = UserBuilder().with_first_name('Bren') \
                            .with_last_name('Magro') \
                            .with_username('breninho') \
                            .with_email('brenoninho@breno.com') \
                            .with_password('123456') \
                            .build()
        user.save()
        self.authenticate_user(user, '123456')
        data = {'thought': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in lectus vitae elit congue interdum sed ut quam. Vivamus at lectus lacus. Proin fringilla porta sapien, vel scelerisque quam aliquet at. Integer faucibus justo nibh, sodales placerat eros consectetur sed. Praesent ultrices felis arcu, at luctus turpis auctor fermentum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in lectus vitae elit congue interdum sed ut quam. Vivamus at lectus lacus. Proin fringilla porta sapien, vel scelerisque quam aliquet at. Integer faucibus justo nibh, sodales placerat eros consectetur sed. Praesent ultrices felis arcu, at luctus turpis auctor fermentum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in lectus vitae elit congue interdum sed ut quam. Vivamus at lectus lacus. Proin fringilla porta sapien, vel scelerisque quam aliquet at. Integer faucibus justo nibh, sodales placerat eros consectetur sed. Praesent ultrices felis arcu, at luctus turpis auctor fermentum.'}
        url = reverse('thought-list')

        response = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, Thought.objects.count())

    def test_should_list_user_thoughts(self):
        first_user = UserBuilder().with_first_name('Bren') \
                                  .with_last_name('Magro') \
                                  .with_username('breninho') \
                                  .with_email('brenoninho@breno.com') \
                                  .with_password('123456') \
                                  .build()
        first_user.save()
        second_user = UserBuilder().with_first_name('Extra')\
                                  .with_last_name('User')\
                                  .with_username('extra')\
                                  .with_email('extra@user.com')\
                                  .with_password('123456')\
                                  .build()
        second_user.save()

        thought = ThoughtBuilder().with_thought('Adipiscing ipsum dolor sit.')\
                                  .with_owner(first_user)\
                                  .build()
        thought.save()
        thought = ThoughtBuilder().with_thought('Lorem ipsum dolor sit.')\
                                  .with_owner(second_user)\
                                  .build()
        thought.save()
        thought = ThoughtBuilder().with_thought('consectetur adipiscing.')\
                                  .with_owner(second_user)\
                                  .build()
        thought.save()

        response = self.client.get(
            reverse('thought-list'),
            {'username': second_user.username},
            format='json'
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data['results']), 2)
        self.assert_response_thought(
            {
                'thought': 'Lorem ipsum dolor sit.',
                'user': {'username': second_user.username}
            },
            response.data['results'][0]
        )
        self.assert_response_thought(
            {
                'thought': 'consectetur adipiscing.',
                'user': {'username': second_user.username}
            },
            response.data['results'][1]
        )

    def test_should_not_list_thoughts_if_user_filter_is_missing(self):
        response = self.client.get(reverse('thought-list'), format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_should_read_thought(self):
        user = UserBuilder().with_first_name('Bren') \
                                  .with_last_name('Magro') \
                                  .with_username('breninho') \
                                  .with_email('brenoninho@breno.com') \
                                  .with_password('123456') \
                                  .build()
        user.save()
        thought = ThoughtBuilder().with_thought('Adipiscing ipsum dolor sit.')\
                                  .with_owner(user)\
                                  .build()
        thought.save()

        response = self.client.get(
            reverse('thought-detail', kwargs={'pk': thought.id}),
            {'username': user.username},
            format='json'
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assert_response_thought(
            {
                'thought': 'Adipiscing ipsum dolor sit.',
                'user': {'username': user.username}
            },
            response.data
        )
