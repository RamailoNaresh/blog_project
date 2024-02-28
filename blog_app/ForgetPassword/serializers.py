from rest_framework import serializers
from blog_app.models import ForgetPassword

class ForgetPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForgetPassword
        fields = "__all__"

class ChangePasswordSerializer(serializers.Serializer):
    password= serializers.CharField(max_length = 255)