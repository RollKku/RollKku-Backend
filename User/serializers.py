from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=45)
    name = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(required=True, max_length=64)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=45)
    password = serializers.CharField(required=True, max_length=64)
