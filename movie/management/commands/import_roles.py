import json
from datetime import datetime
from itertools import islice

from django.utils import timezone
from django.core.management.base import BaseCommand
from slugify import slugify
from movie.models import Role

role_list = ['продюсер','режиссёр','оператор','композитор','специалист по освещению','художник-постановщик','декоратор','гримёр','костюмер','актёр', 'сценарист']


class Command(BaseCommand):
    help = 'import roles to django database'

    def handle(self, *args, **options):

        for i in role_list:
            genre, created = Role.objects.get_or_create(
                name = i
            )

            if created:
                genre.save()
            else:
                self.stdout.write(f'Genre is already exists: {i}')
        
        self.stdout.write(self.style.SUCCESS(f'Roles imported'))

    
