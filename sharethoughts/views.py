from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from iam.exceptions import UsernameError
from sharethoughts.models import Thought
from sharethoughts.serializers import ThoughtSerializer


class ThoughtListView(generics.ListCreateAPIView):
    serializer_class = ThoughtSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        try:
            return super(ThoughtListView, self).list(request, *args, **kwargs)
        except UsernameError:
            data = {
                'error': 'Bad Request (400)',
                'message': 'You must filter by an username'
            }
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username is not None:
            return Thought.objects.filter(owner__username=username)
        raise UsernameError('fdsfjsda')
