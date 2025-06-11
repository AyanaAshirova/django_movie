from django.db import models
from utils.models import TimeStampAbstractModel
from django.conf import settings
from movie.models import Movie, Person


class MovieSubscription(TimeStampAbstractModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'movie')


class PersonSubscription(TimeStampAbstractModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    person =  models.ForeignKey(Person, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'person')


class Notification(TimeStampAbstractModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=350)
    is_read = models.BooleanField(default=False)