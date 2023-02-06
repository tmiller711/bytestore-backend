from rest_framework import serializers
from .models import Account
from django.contrib.auth import get_user_model

class RegisterAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()