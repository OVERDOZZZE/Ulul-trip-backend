from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, **extra_fields):
        if email is None:
            raise TypeError("Users should have email")
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        return user

    def create_superuser(self, email, password, last_name, first_name, **extra_fields):
        if password is None:
            raise TypeError("Password should not be none")
        user = self.create_user(first_name, last_name, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False, help_text="Email activated")
    is_staff = models.BooleanField(default=False, help_text="Сотрудник")
    is_superuser = models.BooleanField(default=False, help_text="админ")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "last_name",
        "first_name",
    ]
    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
