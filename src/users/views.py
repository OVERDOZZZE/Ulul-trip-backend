import jwt
from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    RegisterSerializer,
    EmailVerifySerializer,
    LoginSerializer,
    RequestResetPasswordEmailSerializer,
    SetNewPasswordSerializer,
    PasswordTokenCheckViewSerializer,
)
from .models import User
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import UserService


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        UserService.send_mail_register(user=user, request=request)
        return Response(data=user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    serializer_class = EmailVerifySerializer
    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as error:
            return Response(
                {"error": "Activation link expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as error:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestResetPasswordEmailView(generics.GenericAPIView):
    serializer_class = RequestResetPasswordEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email", "")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            UserService.send_mail_reset_password(user=user, request=request)
        return Response(
            {"success": "We have sent you link to reset your password"},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckView(generics.GenericAPIView):
    serializer_class = PasswordTokenCheckViewSerializer

    def get(self, request, uidb64, token):
        data = {"uidb64": uidb64, "token": token}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "success": True,
                "message": "Credentials Valid",
                "uidb64": uidb64,
                "token": token,
            },
            status=status.HTTP_200_OK,
        )


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )


def main(request):
    return render(request, "login.html")
