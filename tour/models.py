from django.db import models
from user.models import CustomUser

DURATION_CHOICES = (
    ('1', 'День'),
    ('3', '3 дня'),
    ('7', 'Неделя'),
)
COMPLEXITY_CHOICES = (
    ('Easy', 'Легкий'),
    ('Medium', 'Средний'),
    ('Hard', 'Сложный'),
    ('Extra', 'Экстра-сложный')
)


class Images(models.Model):
    class Meta:
        verbose_name = 'Изображение туров'
        verbose_name_plural = 'Изображения туров'

    image = models.ImageField('Изображение тура', upload_to='media/')
    # tour = models.ForeignKey('Tour', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.image)


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField('Название', max_length=25)
    image = models.ImageField('Изображение', null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    @property
    def get_image(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Place(models.Model):
    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    name_city = models.CharField("Название города", max_length=255)
    name_place = models.CharField('Конкретное место', max_length=255, null=True, blank=True)

    def __str__(self):
        if self.name_place:
            return self.name_place
        else:
            return self.name_city


class Tour(models.Model):
    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    title = models.CharField('Название тура', max_length=25)
    description = models.TextField('Описание тура')
    price = models.FloatField("Цена")
    image = models.ManyToManyField(Images, blank=True, related_name='image_of_tour', verbose_name='Изображения')
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, blank=True, verbose_name='Категория')
    slug = models.SlugField(unique=True)
    date_published = models.DateField(auto_now=True)
    date_departure = models.DateTimeField("Дата и время выезда")
    date_arrival = models.DateTimeField("Дата и время приезда")
    from_place = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name='Откуда', related_name='from_place')
    to = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name='Куда', related_name='to')
    quantity_limit = models.PositiveIntegerField('Лимит', blank=True)
    actual_limit = models.PositiveIntegerField(editable=False, null=True, blank=True)
    is_hot = models.BooleanField('Является горячим', null=True, default=False)
    duration = models.CharField('Длительность', max_length=30, choices=DURATION_CHOICES, default='День')
    complexity = models.CharField('Сложность', max_length=30, choices=COMPLEXITY_CHOICES)

    def __str__(self):
        return self.title

    @property
    def get_image(self):
        try:
            url = self.image.url
        except:
            url =''
        return url


class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    text = models.TextField()
    post = models.ForeignKey(Tour, on_delete=models.CASCADE)
    autor = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.text