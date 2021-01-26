from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


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
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username is not None:
            return Thought.objects.filter(owner__username=username)
        raise UsernameError('fdsfjsda')


class ThoughtDetailView(generics.RetrieveAPIView):
    queryset = Thought.objects.all()
    serializer_class = ThoughtSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, pk, format=None):
        return super(ThoughtDetailView, self).get(request, pk, format)
