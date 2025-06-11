import json
from datetime import datetime
from itertools import islice

from django.utils import timezone
from django.core.management.base import BaseCommand
from slugify import slugify
from movie.models import Country

countries = ["Кыргызстан","США","Великобритания","Франция","Германия","Италия","Испания","Канада","Австралия","Япония","Южная Корея","Китай","Индия","Россия","Бразилия","Мексика","Швеция","Дания","Нидерланды","Новая Зеландия","Аргентина"] 


class Command(BaseCommand):
    help = 'import Countries to django database'

    def handle(self, *args, **options):

        for i in countries:
            genre, created = Country.objects.get_or_create(
                name = i
            )

            if created:
                genre.save()
            else:
                self.stdout.write(f'Country is already exists: {i}')
        
        self.stdout.write(self.style.SUCCESS(f'Countries imported'))

    
