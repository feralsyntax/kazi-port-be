from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.serializers import (ModelSerializer, Serializer, 
                            EmailField, CharField, IntegerField)
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from kazi_app.models import CustomUser


class RegisterUserSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True, min_length=8, 
                        trim_whitespace=False, style={'input_type': 'password'}, 
                        validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['email', 'university', 'course', 'password',]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)