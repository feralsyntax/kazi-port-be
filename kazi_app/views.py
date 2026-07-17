from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

def generate_token(user):
    token = RefreshToken.for_user(user)

    return {
        "message": "Request successful",
        "access_token": str(token.access_token),
        "refresh_token": str(token),
    }