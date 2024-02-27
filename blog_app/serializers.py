from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    accessToken = serializers.CharField()
    refreshToken = serializers.CharField()

    def to_representation(self, instance):
        return {
            "access": str(instance.access_token),
            "refresh": str(instance)
        }