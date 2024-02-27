from rest_framework_simplejwt.tokens import RefreshToken
from blog_app.models import Author
from blog_app.serializers import TokenSerializer
from blog_app.author import author


def generate_token(user):
    refresh = RefreshToken.for_user(user = user)
    serializer = TokenSerializer(refresh)
    return serializer.data

def get_logged_user(id):
    return author.Author.get_author_by_id(id)