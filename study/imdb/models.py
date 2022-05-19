from django.db import models
from django.forms import DecimalField, FloatField
from study import settings


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'User: {self.name}'


class Show(models.Model):
    name = models.CharField('Название', max_length=100)
    year = models.IntegerField('Год')
    poster = models.ImageField(upload_to=settings.STATIC_URL+'imdb/images')
    annotation = models.TextField()
    rating = models.FloatField(blank=True, default=0)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.name


class UserShows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seen = models.BooleanField()
    user_rating = models.IntegerField(blank=True, default=0)
