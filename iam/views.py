from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated

from iam.exceptions import UsernameError, EmailError
from iam.serializers import UserSerializer


class UserListViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super(UserListViewSet, self).create(request, *args, **kwargs)
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


class UserDetailViewSet(mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        if request.user.id != int(kwargs['pk']):
            data = {
                'error': 'Forbidden (403)',
                'message': 'Only the user can see his own information'
            }
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
        return super(UserDetailViewSet, self).retrieve(request, *args, **kwargs)
