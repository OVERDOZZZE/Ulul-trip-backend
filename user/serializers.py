from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = 'username email password password2'.split()
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        user.is_active = False
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if User.objects.filter(email=user.email).exists():
            raise serializers.ValidationError({'email': 'Username with this email already exists'})

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords didn't match"})
        user.set_password(password)
        user.save()
        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ("email",)
