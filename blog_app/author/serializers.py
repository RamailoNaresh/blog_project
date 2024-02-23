from blog_app.models import Author
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ["id", "name", "email", "bio", "role", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
