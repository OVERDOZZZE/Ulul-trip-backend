from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Avatar(models.Model):
    image = models.ImageField()



class CustomUser(AbstractUser):
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, blank=True)