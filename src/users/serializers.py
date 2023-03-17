from django.utils.encoding import force_str
from django.contrib import auth
from django.contrib.auth import password_validation
from django.utils.http import urlsafe_base64_decode

from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username")


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
            "username",
            "email",
            "password",
            "password_again",
        )

    def validate(self, attrs):
        username = attrs.get("username").split(' ')
        for name in username:
            if not name.isalpha() or (name.isalpha() and len(username) != 2):
                raise serializers.ValidationError(
                    f"The users username: {name} should only contain alphabetical characters ex: Ivan Ivanov",
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
    username = serializers.CharField()
    tokens = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    id = serializers.ReadOnlyField()

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
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens(),
        }


class RequestResetPasswordEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=4, max_length=50)

    class Meta:
        model = User
        fields = ("email",)


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

    class Meta:
        fields = ("password", "password_repeat", "uidb64")

    def validate(self, attrs):
        errors = {}
        password = attrs.get("password")
        password_repeat = attrs.get("password_repeat")
        global user
        try:
            uidb64 = attrs.get("uidb64")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            password_validation.validate_password(password=password)
        except exceptions.ValidationError as exc:
            errors["password"] = list(exc.get_codes())
        if errors:
            raise serializers.ValidationError(str(errors))
        if password != password_repeat:
            raise AuthenticationFailed(
                "Make sure that password and password_repeat are the same", 400
            )
        user.set_password(password_repeat)
        user.save()
        return user


class CheckDigitsSerializer(serializers.Serializer):
    digits = serializers.CharField(min_length=6, max_length=6)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ("digits", "uidb64")
