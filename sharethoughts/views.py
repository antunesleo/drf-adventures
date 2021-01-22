from rest_framework import mixins, viewsets

from sharethoughts.models import Thought
from sharethoughts.serializers import ThoughtSerializer


class ThoughtViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Thought.objects.all()
    serializer_class = ThoughtSerializer

# Create your views here.
