from django.db import models
from django.contrib.auth.models import AbstractUser



class Avatar(models.Model):
    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'

    image = models.ImageField(upload_to='media/', null=True)


class CustomUser(AbstractUser):
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, blank=True, null=True, related_name='avatar')