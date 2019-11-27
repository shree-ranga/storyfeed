from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from .serializers import LoginSerializer, LogoutSerializer, RegisterSerializer
from accounts.models import Profile


class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # create profile for new user
            Profile.objects.create(user=serializer.instance)
            # generate token for new user
            token = Token.objects.create(user=serializer.instance)
            return Response(
                {"token": token.key, "id": serializer.instance.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "id": user.id}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    def delete(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
