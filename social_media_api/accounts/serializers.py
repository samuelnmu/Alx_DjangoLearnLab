from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "profile_picture", "followers"]


class RegisterSerializer(serializers.ModelSerializer):
    # Ensure password is write-only and validated properly
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        # Use get_user_model() to allow flexibility with custom models
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        Token.objects.create(user=user)  # generate token for the new user
        return user
