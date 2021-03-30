import logging

from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from iam.exceptions import UsernameError
from thoughts.models import Thought
from thoughts.serializers import ThoughtSerializer


logger = logging.getLogger(__name__)


class ThoughtListView(generics.ListCreateAPIView):
    serializer_class = ThoughtSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        try:
            response = super(ThoughtListView, self).list(request, *args, **kwargs)
            logger.info(f"THOUGHT-VIEW-SET: Listed thoughts, request: {request}.")
            return response
        except UsernameError:
            logger.warning(f"THOUGHT-VIEW-SET: Could not list thoughts, username missing. request: {request}.")
            data = {
                "error": "Bad Request (400)",
                "message": "You must filter by an username"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super(ThoughtListView, self).create(request, *args, **kwargs)
        logger.info(f"THOUGHT-VIEW-SET: Created a thought {request.data}.")
        return response

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username is not None:
            return Thought.objects.filter(owner__username=username)
        raise UsernameError("Username not provided")


class ThoughtDetailView(generics.RetrieveAPIView):
    queryset = Thought.objects.all()
    serializer_class = ThoughtSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, pk, format=None):
        response = super(ThoughtDetailView, self).get(request, pk, format)
        logger.info(f"THOUGHT-VIEW-SET: got Thought {pk}.")
        return response
