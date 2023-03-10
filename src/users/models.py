from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, name, username, email, password, **extra_fields):
        if email is None:
            raise TypeError("Users should have email")
        user = self.model(
            name=name,
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        return user

    def create_superuser(self, email, password, name, username, **extra_fields):
        if password is None:
            raise TypeError("Password should not be none")
        user = self.create_user(name, username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False, help_text="Email activated")
    is_staff = models.BooleanField(default=False, help_text="Сотрудник")
    is_superuser = models.BooleanField(default=False, help_text="админ")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorite_tour = models.ManyToManyField(
        "tour.Tour",
        related_name="favorite_tour",
        verbose_name="Избранные",
    )
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "name",
        "email",
    ]
    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}
