from django.utils.encoding import smart_str, DjangoUnicodeDecodeError, force_str
from django.contrib import auth
from django.contrib.auth import password_validation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import serializers, exceptions, status
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "username")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=30,
        min_length=6,
        write_only=True,
        style={"input_type": "password"},
        validators=[password_validation.validate_password],
        help_text=password_validation.password_validators_help_texts(),
    )
    password_again = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    name = serializers.CharField(
        max_length=50,
        min_length=2,
        help_text="Name should contain only alphabetical characters",
    )
    email = serializers.EmailField(
        max_length=50,
        min_length=3,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        max_length=50,
        min_length=2,
        help_text="Username should contain only alphanumeric characters",
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "username",
            "email",
            "password",
            "password_again",
        )

    def validate(self, attrs):
        name = attrs.get("name", "")
        username = attrs.get("username", "")
        if not name.isalpha() or (name.isalpha() and name.count(" ") == 1):
            raise serializers.ValidationError(
                f"The users  name is not valid, make sure that it contains only alphabetical characters"
            )
        if not username.isalnum():
            raise serializers.ValidationError(
                f"The users username: {username} should only contain alphanumeric characters",
                400,
            )
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password", "")
        password_again = validated_data.pop("password_again", "")
        user = self.Meta.model(**validated_data)
        if password:
            if password == password_again:
                user.set_password(password_again)
            else:
                raise serializers.ValidationError(
                    "Please make sure that password and password_again is the same "
                )
        user.save()
        return user


class EmailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ("token",)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)
    name = serializers.CharField(read_only=True)
    username = serializers.CharField()
    tokens = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        username = attrs.get("username", "")
        password = attrs.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account is disabled, contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")
        return {
            "email": user.email,
            "username": user.username,
            "name": user.name,
            "tokens": user.tokens(),
        }


class RequestResetPasswordEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=4, max_length=50)

    class Meta:
        model = User
        fields = ("email",)


class PasswordTokenCheckViewSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ("uidb64", "token")

    def validate(self, attrs):
        uidb64 = attrs.get("uidb64")
        token = attrs.get("token")
        global user
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.filter(id=id).first()
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token is not valid, please request a new one"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Invalid credentials were provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token is not valid please request new one"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6,
        max_length=30,
        write_only=True,
        help_text=password_validation.password_validators_help_texts(),
    )
    password_repeat = serializers.CharField(
        min_length=6, max_length=30, write_only=True
    )
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ("password", "password_repeat", "uidb64", "token")

    def validate(self, attrs):
        errors = {}
        password = attrs.get("password")
        password_repeat = attrs.get("password_repeat")
        global user, token
        try:
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            password_validation.validate_password(password=password)
        except exceptions.ValidationError as exc:
            errors["password"] = list(exc.get_codes())
        except Exception as e:
            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                raise AuthenticationFailed("This reset link is invalid", 401)
        if errors:
            raise serializers.ValidationError(str(errors))
        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
            raise AuthenticationFailed("This reset link is invalid", 404)
        if password != password_repeat:
            raise AuthenticationFailed(
                "Make sure that password and password_repeat are the same", 400
            )
        user.set_password(password_repeat)
        user.save()
        return user
