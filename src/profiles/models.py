from django.db import models
from src.users.models import User
from pytils import translit

CHOICES = (
    ('⭐', '1'),
    ('⭐⭐', '2'),
    ('⭐⭐⭐', '3'),
    ('⭐⭐⭐⭐', '4'),
    ('⭐⭐⭐⭐⭐', '5'),
)


class BaseModel(models.Model):
    objects = models.Manager


class UserReview(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True,db_index=True,)
    review = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        default=''

    )
    rate = models.IntegerField(
        choices=CHOICES,
        null=True,
        blank=True,
        default=0
    )

    @property
    def get_user(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = translit.slugify(self.get_user)
        super(UserReview, self).save(*args,**kwargs)

    def __str__(self):
        return self.review
