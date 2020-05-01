from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

User = get_user_model()

# create profile here instead of views
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ["username", "full_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField()

    class Meta:
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data.get("username", None)
        email = data.get("email", None)
        password = data.get("password")

        try:
            user_obj = User.objects.filter(Q(email=email) | Q(username=username))[0]
        except:
            raise ValidationError("Invalid Username/Email.")

        user = authenticate(username=user_obj.username, password=password)

        if user is not None:
            data["user"] = user
        else:
            msg = "Invalid Password."
            raise ValidationError(msg)

        return data


class LogoutSerializer(serializers.Serializer):
    pass


class PasswordChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        password = validated_data.get("password", "")
        instance.set_password(password)
        instance.save()
        return instance
