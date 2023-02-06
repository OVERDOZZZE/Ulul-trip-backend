from django.db import models
from user.models import CustomUser

DURATION_CHOICES= (
    ('1', 'День'),
    ('3', '3 дня'),
    ('7','Неделя'),
)
COMPLEXITY_CHOICES = (
    ('Easy', 'Легкий'),
    ('Meduim', 'Средний'),
    ('Hard','Сложный'),
    ('Extra','Экстра-сложный')
)
class Category(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField()
    slug = models.SlugField()

class Place(models.Model):
    name_city = models.CharField()
    name_place = models.CharField(null=True)



class Tour(models.Model):
    title = models.CharField(max_lenght=25)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField()
    category = models.ForeignKey(Category, null=True)
    slug = models.SlugField()
    date_publishied = models.DateField()
    date_departure = models.DateTimeField()
    date_arrival = models.DateTimeField()
    from_ = models.ForeignKey(Place)
    to = models.ForeignKey(Place)
    quantity_limit = models.PositiveIntegerField()
    actual_limit = models.PositiveIntegerField()
    is_hot = models.BooleanField(null=True, default=False)
    duration_field = models.CharField(choices=DURATION_CHOICES)
    complexity = models.CharField(choices=COMPLEXITY_CHOICES)

class Review(models.Model):
    text = models.TextField
    post = models.ForeignKey(Tour)
    autor = models.OneToOneField(CustomUser)


