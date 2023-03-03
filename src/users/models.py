from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.safestring import mark_safe
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import path_and_rename3
from pytils import translit


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, name, email, password, number):
        if email is None:
            raise TypeError('Users should have email')
        user = self.model(username=username, name=name, email=self.normalize_email(email), number=number)
        user.set_password(password)
        return user

    def create_superuser(self, email, password, username, name, number):
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(username, name, email, password, number)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    number = models.CharField(max_length=255, db_index=True)
    image = models.ImageField(upload_to=path_and_rename3, blank=True, null=True,
                              default='user_images/default_image/default_user_image.jpeg')
    user_slug = models.SlugField(max_length=100,db_index=True,unique=True,verbose_name='URl')
    is_verified = models.BooleanField(default=False,help_text='Email activated')
    is_staff = models.BooleanField(default=False,help_text='Сотрудник')
    is_superuser = models.BooleanField(default=False,help_text='админ')
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'number']
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.user_slug = translit.slugify(self.username)
        super(User, self).save(*args, **kwargs)

    @property
    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "60" height = "60"/>')
        return 'None'

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
