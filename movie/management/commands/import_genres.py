import os

from django.core.management.base import BaseCommand
from tmdbv3api import TMDb, Genre as TMDbGenre
from Movies.models import Genre


class Command(BaseCommand):
    help = 'import TMDB genres to django database'

    def handle(self, *args, **options):
        tmdb = TMDb()
        # tmdb.api_key = os.getenv('TMDB_API_KEY')
        tmdb.api_key = '9fa12374bfa1ee4104add97410cc9f5c'

        genre_api = TMDbGenre()
        genres = genre_api.movie_list()

        for g in genres:
            genre, created = Genre.objects.get_or_create(
                tmvdbid=g.id,
            )

            if created:
                genre.name = g.name
                genre.save()
                self.stdout.write(f'Genre is already exists: {g.name}')
            else:
                self.stdout.write(self.style.SUCCESS(f'Genre created: {g.name}'))
