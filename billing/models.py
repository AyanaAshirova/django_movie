from django.db import models
from django.conf import settings
from movie.models import Movie

class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription', verbose_name='Пользователь')
    start_date = models.DateField(auto_now_add=True, verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchases', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,related_name='purchases', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')

    class Meta:
        unique_together = ('user', 'movie')



