import json
from datetime import datetime
from itertools import islice

from django.utils import timezone
import pandas as pd
from django.core.management.base import BaseCommand
from slugify import slugify
import numpy as np
from Movies.models import Movies as MoviesModel
from Movies.models import Genre


class Command(BaseCommand):
    help = 'Import movies from csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='path to csv file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        try:
            df_set = pd.read_csv(csv_file)
            now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())


            for i, row in df_set.iterrows():
                tmdb_id = int(row['id'])
                title = row['original_title']

                movie, created = MoviesModel.objects.get_or_create(tmvdbid=tmdb_id)

                if created:
                    genres = []
                    for g in json.loads(row['genres']):
                        genre, created = Genre.objects.get_or_create(
                            tmvdbid=int(g['id']),
                            defaults={
                                'name': g['name']
                            }
                        )
                        genres.append(genre.id)

                    if row['release_date']:
                        parsed_date = datetime.strptime(row['release_date'], '%Y-%m-%d').date()
                        movie.release_date = parsed_date

                    movie.genres.set(genres)
                    movie.tmdb_id = tmdb_id
                    movie.name = title
                    slug_text = slugify(title)+'_'+slugify(str(np.random.randint(0, 100)))
                    movie.slug = slug_text
                    movie.date = now
                    movie.save()

                    self.stdout.write(f'{i}: Created -----> {title} - {tmdb_id}')
                else:
                    self.stdout.write(self.style.WARNING(f'{i}: Movies already exists: {title} - {tmdb_id}'))

            self.stdout.write(self.style.SUCCESS('Successfully imported movies'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CSV file not found'))
