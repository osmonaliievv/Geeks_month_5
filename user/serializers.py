from . import models
from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
    password_confirm = serializers.CharField(min_length=6)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def validate_username(self, username):
        try:
            User.objects.filter(username=username).exists()
        except User.DoesNotExist:
            return username
        raise serializers.ValidationError("Username already exists")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)


class SMSCodeSerializer(serializers.Serializer):
    sms_code = serializers.CharField(max_length=6)
