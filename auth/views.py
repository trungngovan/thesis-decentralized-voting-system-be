from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request=RegisterSerializer,
        responses={201: {"description": "User registered successfully."}},
        description="Register user",
        tags=["Authentication"],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"message": "User registered successfully.", "token": token.key},
            status=status.HTTP_201_CREATED,
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {"description": "Login successful."},
            401: {"description": "Invalid credentials."},
        },
        description="Login user",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({"token": token.key, "message": "Login successful."})
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            200: {"description": "Logout successful."},
            401: {"description": "Not authenticated."},
        },
        description="Logout user",
    )
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Logout successful."})


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: {"description": "Password changed successfully."},
            400: {"description": "Invalid old password."},
            401: {"description": "Not authenticated."},
        },
        description="Change user password",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
