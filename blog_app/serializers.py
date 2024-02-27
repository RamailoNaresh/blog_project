from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

    def to_representation(self, instance):
        return {
            "access": str(instance.access_token),
            "refresh": str(instance)
        }