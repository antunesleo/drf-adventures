from django.contrib.auth.models import User
from rest_framework import serializers

from sharethoughts.models import Thought


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('user-detail')

    class Meta:
        model = User
        fields = ('username', 'url')


class ThoughtSerializer(serializers.HyperlinkedModelSerializer):
    thought = serializers.CharField(max_length=800)
    created_at = serializers.DateTimeField(read_only=True)
    user = UserSerializer(source='owner', read_only=True)
    url = serializers.HyperlinkedIdentityField('thought-detail')

    class Meta:
        fields = ['thought', 'created_at', 'user', 'url']
        model = Thought

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(ThoughtSerializer, self).create(validated_data)
