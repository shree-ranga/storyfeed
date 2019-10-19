from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    full_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "full_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        full_name = validated_data.pop("full_name")
        split_name = full_name.rsplit(None, 1)
        first_name = split_name[0]
        last_name = split_name[1]
        validated_data["first_name"] = first_name
        validated_data["last_name"] = last_name
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)


class LogoutSerializer(serializers.Serializer):
    pass


class PasswordChangeSerializer(serializers.ModelSerializer):
    pass


class PasswordResetSerializer(serializers.ModelSerializer):
    pass

