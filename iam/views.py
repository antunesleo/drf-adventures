from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import bad_request

from iam.exceptions import UsernameError, EmailError
from iam.serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super(UserViewSet, self).create(request, *args, **kwargs)
        except UsernameError:
            data = {
                'error': 'Bad Request (400)',
                'message': 'Username already in use'
            }
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        except EmailError:
            data = {
                'error': 'Bad Request (400)',
                'message': 'Email already in use'
            }
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
