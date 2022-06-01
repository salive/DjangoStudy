from django.db import models
from django.forms import FloatField
from study import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


class Show(models.Model):
    title = models.CharField('Название', max_length=100)
    year = models.IntegerField('Год')
    poster = models.ImageField(
        'Постер', upload_to=settings.STATIC_URL+'imdb/images')
    description = models.TextField('Описание')
    rating = models.FloatField('Рейтинг', blank=True, default=0)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title


class UserShows(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    show = models.ForeignKey(
        Show, related_name='user_show', on_delete=models.CASCADE)
    seen = models.BooleanField(null=True, blank=True)
    user_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10), MinValueValidator(0)])

    class Meta:
        verbose_name = 'Пользовательский фильм'
        verbose_name_plural = 'Пользовательские фильмы'

    def __str__(self):
        return f'{self.user}: {self.show}'
