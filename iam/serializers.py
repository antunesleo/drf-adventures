from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from iam.exceptions import UsernameError, EmailError


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

    def create(self, validated_data):
        users = User.objects.filter(username=validated_data['username'])
        if users:
            username = validated_data['username']
            raise UsernameError(f'the user {username} is already in use')

        users = User.objects.filter(email=validated_data['email'])
        if users:
            email = validated_data['email']
            raise EmailError(f'the email {email} is already in use')

        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
