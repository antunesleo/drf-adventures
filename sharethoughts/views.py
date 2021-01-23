from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from sharethoughts.models import Thought
from sharethoughts.serializers import ThoughtSerializer


class ThoughtViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Thought.objects.all()
    serializer_class = ThoughtSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
