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
    is_series = models.BooleanField()
    num_seasons = models.IntegerField('Number of seasons', validators=[
                                      MinValueValidator(0)], blank=True, null=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title


class Season(models.Model):
    show = models.ForeignKey(
        Show, on_delete=models.CASCADE, related_name='series')
    season_number = models.IntegerField(
        'Season number', validators=[MinValueValidator(0)])
    num_episodes = models.IntegerField(
        'Number of episodes', validators=[MinValueValidator(0)])
    air_date = models.DateField('Air date', blank=True, null=True)

    def __str__(self):
        return f'{self.show}: season {self.season_number}'


class Episode(models.Model):
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name='season')
    episode_number = models.IntegerField(
        'Episode number', validators=[MinValueValidator(0)])
    titleRu = models.CharField(
        'TitleRU', max_length=100, null=True, blank=True)
    titleEn = models.CharField(
        'TitleEN', max_length=100, null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    air_date = models.DateField('Air date', null=True, blank=True)

    def __str__(self):
        return f'{self.season}: episode {self.episode_number}'


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
