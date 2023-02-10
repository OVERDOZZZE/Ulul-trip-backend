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
    image = models.ImageField(blank=True)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name

class PlaceFrom(models.Model):
    name_city = models.CharField(max_length=25)
    name_place = models.CharField(max_length=25, null=True)

class PlaceTo(models.Model):
    name_city = models.CharField(max_length=25)
    name_place = models.CharField(max_length=25, null=True)




class Tour(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, blank=True)
    slug = models.SlugField(unique=True)
    date_publishied = models.DateField(auto_now=True)
    date_departure = models.DateTimeField()
    date_arrival = models.DateTimeField()
    from_place = models.ForeignKey(PlaceFrom, on_delete=models.CASCADE)
    to = models.ForeignKey(PlaceTo, on_delete=models.CASCADE)
    quantity_limit = models.PositiveIntegerField(blank=True)
    actual_limit = models.PositiveIntegerField(editable=False)
    is_hot = models.BooleanField(null=True, default=False)
    duration_field = models.CharField(max_length=30, choices=DURATION_CHOICES)
    complexity = models.CharField(max_length=30, choices=COMPLEXITY_CHOICES)
    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField
    post = models.ForeignKey(Tour, on_delete=models.CASCADE)
    autor = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.text


