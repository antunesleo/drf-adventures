from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse


class AuthenticableTestMixin(TestCase):

    def authenticate_user(self, user: User, text_password: str):
        credentials = {
            'username': user.username,
            'password': text_password
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, credentials, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
