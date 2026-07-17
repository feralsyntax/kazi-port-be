from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.serializers import (ModelSerializer, Serializer, 
                            EmailField, CharField)
from rest_framework.exceptions import AuthenticationFailed
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
    

class LoginUserSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password
        )

        if not user:
            raise AuthenticationFailed("Invalid email or password")

        attrs["user"] = user
        return attrs