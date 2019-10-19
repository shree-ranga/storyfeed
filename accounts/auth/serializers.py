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

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        full_name = ret.pop("full_name")
        split_name = full_name.rsplit(None, 1)
        first_name = split_name[0]
        last_name = split_name[1]
        ret["first_name"] = first_name
        ret["last_name"] = last_name
        return ret

    def create(self, validated_data):
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

