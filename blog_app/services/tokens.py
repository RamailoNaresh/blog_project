from rest_framework_simplejwt.tokens import RefreshToken
from blog_app.serializers import TokenSerializer


def generate_token(user):
    refresh = RefreshToken.for_user(user)
    serializer = TokenSerializer(refresh)
    return serializer.data