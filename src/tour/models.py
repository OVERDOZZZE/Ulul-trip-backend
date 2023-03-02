from src.users.models import User
from django.db import models


class Guide(models.Model):
    class Meta:
        verbose_name = "Guide"
        verbose_name_plural = "Guides"

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="media/guides", blank=True)
    slug = models.SlugField(unique=True)

    def get_initials(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.get_initials()


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review_author"
    )
    post = models.ForeignKey(
        "Tour", on_delete=models.CASCADE, related_name="tour_reviews"
    )
    rating = models.SmallIntegerField(choices=RATING_CHOICES, default=5)
    date_published = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Region(models.Model):
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name


class Images(models.Model):
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    image = models.ImageField(upload_to="media/")
    tour = models.ForeignKey(
        "Tour", on_delete=models.CASCADE, related_name="tour_images"
    )
    is_main = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.image)


class Tour(models.Model):
    class Meta:
        verbose_name = "Tour"
        verbose_name_plural = "Tours"

    DURATION_CHOICES = (("1", "День"), ("3", "3 дня"), ("7", "7 дней"))

    COMPLEXITY_CHOICES = (
        ("Easy", "Легкий"),
        ("Medium", "Средний"),
        ("Hard", "Тяжелый"),
        ("Extra", "Экстра"),
    )

    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    price = models.SmallIntegerField("Цена")
    slug = models.SlugField(unique=True)
    date_published = models.DateField(auto_now=True)
    date_departure = models.DateField()
    date_arrival = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    quantity_limit = models.PositiveIntegerField(blank=True)
    actual_limit = models.PositiveIntegerField(editable=False, blank=True, null=True)
    is_hot = models.BooleanField(default=False)
    duration = models.CharField(max_length=255, choices=DURATION_CHOICES)
    complexity = models.CharField(max_length=255, choices=COMPLEXITY_CHOICES)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        count = self.tour_reviews.count()
        if count == 0:
            return f"No reviews yet"
        total = 0
        for i in self.tour_reviews.all():
            total += i.rating
        return total / count

    def set_actual_limit(self):
        self.actual_limit = self.quantity_limit
        return self.actual_limit
