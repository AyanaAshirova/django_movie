from django.db import models
from movie.models import Movie
from django.contrib.auth.models import User

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    start_date = models.DateField(auto_now_add=True, verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')


class Purchase(models.Model):
    user = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')

    class Meta:
        unique_together = ('user', 'movie')


