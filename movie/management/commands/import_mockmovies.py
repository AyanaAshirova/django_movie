import os

from django.core.management.base import BaseCommand
from movie.models import *
from slugify import slugify


class Command(BaseCommand):
    help = 'Import mock movies to Django database'

    def handle(self, *args, **options):
        countries = ["Кыргызстан","США","Великобритания","Франция","Германия","Италия","Испания","Канада","Австралия","Япония","Южная Корея","Китай","Индия","Россия","Бразилия","Мексика","Швеция","Дания","Нидерланды","Новая Зеландия","Аргентина"] 
        genres = ['Комедия','Мультфильм','Ужас','Фантастика','Триллер','Боевик','Мелодрама','Детектив','Приключение','Фэнтези','Военный','Семейный','Аниме','Исторический','Драма','Документальный','Криминал','Биография','Вестерн','Фильм-нуар','Спортивный','Короткометражка','Музыкальный','Мюзикл', 'Лайв-адаптация']
        roles = ['продюсер','режиссёр','оператор','композитор','специалист по освещению','художник-постановщик','декоратор','гримёр','костюмер','актёр', 'сценарист']

        # Создание стран
        country_objects = {}
        for name in countries:
            country, _ = Country.objects.get_or_create(name=name)
            country_objects[name] = country

        # Создание жанров
        genre_objects = {}
        for name in genres:
            genre, _ = Genre.objects.get_or_create(name=name)
            genre_objects[name] = genre

        role_objects = {}
        for name in roles:
            role, _ = Role.objects.get_or_create(name=name)
            role_objects[name] = role

        # Пример людей и ролей
        people_data = [
            {'name': 'Иван Иванов', 'roles': ['актер', 'режиссёр']},
            {'name': 'Мария Смирнова', 'roles': ['продюсер']},
            {'name': 'Дмитрий Петров', 'roles': ['оператор']},
        ]

        person_roles_objects = []
        for person_data in people_data:
            person, _ = Person.objects.get_or_create(name=person_data['name'])
            role_objs = Role.objects.filter(name__in=person_data['roles'])
            person_role, _ = PersonRole.objects.get_or_create(person=person)
            person_role.roles.set(role_objs)
            person_role.save()
            person_roles_objects.append(person_role)

        # Пример фильмов
        movies = [
            {
                'title': 'Побег из Шоушенка',
                'release_date': '1994-09-23',
                'country': "США",
                'genres': ['Комедия','Мультфильм','Ужас'],
                'description': 'История о надежде и дружбе в тюрьме.',
                'movie_length': 142,
                'persons': person_roles_objects[:2],
                'trailer_url': 'https://www.youtube.com/watch?v=NmzuHjWmXOc',
            },
            {
                'title': 'Интерстеллар',
                'release_date': '2014-11-07',
                'country': "США",
                'genres': ['Комедия','Мультфильм','Ужас'],
                'description': 'Путешествие сквозь космос в поисках нового дома.',
                'movie_length': 169,
                'persons': person_roles_objects[1:],
                'trailer_url': 'https://www.youtube.com/watch?v=zSWdZVtXT7E',
            },
            {
                'title': 'Амели',
                'release_date': '2001-04-25',
                'country': "Германия",
                'genres': ['Комедия','Мультфильм','Ужас'],
                'description': 'История о девушке, меняющей жизни людей вокруг.',
                'movie_length': 122,
                'persons': person_roles_objects[:1],
                'trailer_url': 'https://www.youtube.com/watch?v=HUECWi5pX7o',
            },
            {
                'title': 'Старикам здесь не место',
                'release_date': '2007-11-09',
                'country': "Германия",
                'genres': ['Комедия','Мультфильм','Ужас'],
                'description': 'Смертельная игра в пустынях Техаса.',
                'movie_length': 122,
                'persons': person_roles_objects[2:],
                'trailer_url': 'https://www.youtube.com/watch?v=38A__WT3-o0',
            },
            {
                'title': 'Принцесса Мононоке',
                'release_date': '1997-07-12',
                'country': "Германия",
                'genres': ['Комедия','Мультфильм','Ужас'],
                'description': 'Эпическая битва между природой и цивилизацией.',
                'movie_length': 134,
                'persons': person_roles_objects[:2],
                'trailer_url': 'https://www.youtube.com/watch?v=4OiMOHRDs14',
            },
            {
                'title': 'Город Бога',
                'release_date': '2002-02-13',
                'country': "Германия",
                'genres': ['Комедия','Мультфильм','Ужас'],
                'description': 'Жестокая реальность трущоб Рио-де-Жанейро.',
                'movie_length': 130,
                'persons': person_roles_objects[1:],
                'trailer_url': 'https://www.youtube.com/watch?v=dcUOO4Itgmw',
            },
        ]

        for movie_data in movies:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'release_date': datetime.strptime(movie_data['release_date'], '%Y-%m-%d').date(),
                    'description': movie_data['description'],
                    'movie_length': movie_data['movie_length'],
                    'trailer_url': movie_data['trailer_url'],
                    'premium': False,
                    'country': country_objects[movie_data['country']],
                }
            )

            if created:
                movie.genres.set([genre_objects[g] for g in movie_data['genres']])
                movie.persons.set(movie_data['persons'])
                print(movie)
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"Movie imported: {movie.title}"))
            else:
                self.stdout.write(f"Movie already exists: {movie.title}")