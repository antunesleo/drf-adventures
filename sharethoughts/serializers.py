from rest_framework import serializers

from sharethoughts.models import Thought


class ThoughtSerializer(serializers.ModelSerializer):
    thought = serializers.CharField(max_length=800)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        fields = ['thought', 'created_at']
        model = Thought
