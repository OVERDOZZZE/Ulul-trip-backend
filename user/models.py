from django.db import models

# Create your models here.

class Avatar(models.Model):
    image = models.ImageField()



class CustomUser(models.User):
    avatar = models.ForeignKey(Avatar)