import os

from django.core.management.base import BaseCommand
from movie.models import Genre


genre_list = ['Комедия','Мультфильм','Ужас','Фантастика','Триллер','Боевик','Мелодрама','Детектив','Приключение','Фэнтези','Военный','Семейный','Аниме','Исторический','Драма','Документальный','Криминал','Биография','Вестерн','Фильм-нуар','Спортивный','Короткометражка','Музыкальный','Мюзикл', 'Лайв-адаптация']
# 'Ток-шоу'



class Command(BaseCommand):
    help = 'import genres to django database'

    def handle(self, *args, **options):
      

        for i in genre_list:
            genre, created = Genre.objects.get_or_create(
                name = i
            )

            if created:
                genre.save()
            else:
                self.stdout.write(f'Genre is already exists: {i}')

        self.stdout.write(self.style.SUCCESS(f'Genre imported'))
