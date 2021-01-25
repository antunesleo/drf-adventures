from django.test import TestCase
from rest_framework.reverse import reverse

from common.testing.builders import UserBuilder


class AuthenticableTestMixin(TestCase):

    def setUp(self) -> None:
        self.password = '123465'
        self.auth_user = UserBuilder().with_first_name('Breno')\
                                      .with_last_name('Magro')\
                                      .with_username('breno')\
                                      .with_email('breno@breno.com')\
                                      .with_password(self.password)\
                                      .build()
        self.auth_user.save()

    def obtain_and_configure_access_token(self):
        credentials = {
            'username': self.auth_user.username,
            'password': self.password
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, credentials, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
