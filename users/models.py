from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name='фото профиля')
    birth_date = models.DateField(null=True, blank=True, verbose_name='дата рождения')

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = f'avatars/default-{randint(1, 5)}.jpg'
        super().save(*args, **kwargs)


