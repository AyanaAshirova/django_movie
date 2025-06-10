from django.db import models


class TimeStampAbstractModel(models.Model):
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True
