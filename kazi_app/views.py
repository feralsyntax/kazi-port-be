from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView

from kazi_app.serializers import LoginUserSerializer, RegisterUserSerializer

# Create your views here.

def generate_token(user):
    token = RefreshToken.for_user(user)

    return {
        "message": "Request successful",
        "access_token": str(token.access_token),
        "refresh_token": str(token),
    }


@permission_classes([AllowAny,])
class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            generate_token(user),
            status=status.HTTP_201_CREATED
        )


@permission_classes([AllowAny,])
class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        return Response(generate_token(user))