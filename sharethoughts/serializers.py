from rest_framework import serializers

from sharethoughts.models import Thought


class ThoughtSerializer(serializers.ModelSerializer):
    thought = serializers.CharField(max_length=800)
    created_at = serializers.DateTimeField(read_only=True)
    username = serializers.SlugRelatedField(
        source='owner',
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ['thought', 'created_at', 'username']
        model = Thought

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(ThoughtSerializer, self).create(validated_data)
