from django.db import models
from django.forms import FloatField
from study import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Show(models.Model):
    title = models.CharField('Название', max_length=100)
    year = models.IntegerField('Год')
    poster = models.ImageField(upload_to=settings.STATIC_URL+'imdb/images')
    description = models.TextField()
    rating = models.FloatField(blank=True, default=0)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shows = models.ManyToManyField(Show, related_name='shows')

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
