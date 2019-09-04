from rest_framework import serializers
from .models import CustomUser


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class ActivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_active']
