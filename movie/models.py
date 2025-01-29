from datetime import datetime
from django.db import models
from django.core.validators import FileExtensionValidator

from slugify import slugify
from .account.models import User

ROLE_CHOICES = [
    ('actor', 'Актер'),
    ('derctor', 'Режиссер'),
    ('producer', 'Продюсер'),
    ('writer', 'Сценарист'),
    ('composer', 'Композитор'),
    ('operator', 'Оператор')
]

class Role(models.Model):
    name = models.CharField(max_length=20, verbose_name='Роль')

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=1000, verbose_name='Имя')
    photo = models.ImageField(upload_to='persons/', verbose_name='Фотографии')
    movies = models.ManyToManyField('Movie', related_name='movies', verbose_name='Фильмы')
    roles = models.ManyToManyField(Role, verbose_name='Роли')

    def __str__(self):
        return self.name



class PersonRole(models.Model):
    person = models.ForeignKey(Person, related_name='Человек')
    roles = models.ManyToManyField(Role, verbose_name='Роли')


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Raiting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='raitings', verbose_name='Фильм')
    value = models.PositiveBigIntegerField(choices=[(i, i) for i in range(1, 11)], verbose_name='Оценка')

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.user} - {self.movie} : {self.value}'



class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    genres = models.ManyToManyField(Genre, related_name='movies', verbose_name='Жанры')
    slug = models.SlugField(max_length=120, blank=True, unique=True)
    premium = models.BooleanField(default=False)
    description = models.TextField(max_length=10000, null=True, blank=True, verbose_name='Описание')
    movie_length = models.PositiveBigIntegerField(verbose_name='Длительность в минутах')
    release_date = models.DateField(verbose_name='Дата выхода')
    persons = models.ManyToManyField(PersonRole, verbose_name='Люди')
    screen_shot = models.ImageField(upload_to='movies/screenshots/', null=True, blank=True, verbose_name='Кадры из фильма')
    poster = models.ImageField(upload_to='movies/posters/', blank=True, default='default.jpg')
    bg_photo = models.ImageField(upload_to='movies/bg_photos', blank=True, null=True)
    price = models.PositiveBigIntegerField(null=True)

    video_720 = models.FileField(
        upload_to='movies/videos/720/', 
        null=True, blank=True, 
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    video_1920 = models.FileField(
        upload_to='movies/videos/1920/', 
        null=True, blank=True, 
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    video_4k = models.FileField(
        upload_to='movies/videos/4k/', 
        null=True, blank=True, 
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    
    created_at = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def get_duration_dispaly(self):
        hours = self.movie_length // 60
        min = self.movie_length % 60
        return f'{hours}ч. {min}мин' if hours else f'{min}мин'

    def average_rating(self):
        raitings = self.raitings.all()
        if raitings.exists():
            return round(sum(raiting.value for raiting in raitings) / raitings.count(), 2)
        return 0

    def __str__(self):
        return f'{self.name} - {self.release_date}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super (Movie, self).save(*args, **kwargs)

    def snippet(self):
        return self.discription[:10]+'...'


class MovieFrame(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='frames')
    frame_image = models.ImageField(upload_to='frames/')


class NewTrailer(models.Model):
    title = models.CharField(max_length=1000, null=True, blank=True)
    link = models.CharField(max_length=1500, null=True, blank=True)
    discription = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ImageField(upload_to='trailer_image', null=True, blank=True)
    image_link = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    def snipet(self):
        return self.discription[:70] + '...'



# class SeriesModel(models.Model):
#     name = models.CharField(max_length=500)
#     discription = models.TextField(max_length=10000, null=True, blank=True)
#     image = models.ImageField(upload_to='images/', null=True, blank=True)
#     screen_shot = models.ImageField(upload_to='screenshots/', null=True, blank=True)
#     series_length = models.CharField(max_length=50, null=True, blank=True)
#     release_date = models.DateField()
#     series_rate = models.CharField(max_length=100, null=True, blank=True)
#     imdb_rating = models.CharField(max_length=100, null=True, blank=True)
#     series_director = models.CharField(max_length=200, null=True, blank=True)
#     series_actor = models.CharField(max_length=1000, null=True, blank=True)
#     series_language = models.CharField(max_length=100, null=True, blank=True)
#     series_quality = models.CharField(max_length=100, null=True, blank=True)
#     series_size = models.CharField(max_length=100, null=True, blank=True)
#     series_subtitle = models.CharField(max_length=100, null=True, blank=True)
#     series_type = models.CharField(max_length=200, null=True, blank=True)
#     series_subscription = models.CharField(max_length=700, null=True, blank=True)
#     series_category = models.CharField(max_length=100, null=True, blank=True)
#     date = models.DateTimeField()
#     seasons = models.CharField(max_length=1000, null=True, blank=True)

#     def __str__(self):
#         return self.name

#     def snipet(self):
#         return self.discription[:100] + '...'


# class season(models.Model):
#     selected_season = models.IntegerField(null=True, blank=True)
#     episode = models.IntegerField(null=True, blank=True)
#     series = models.OneToOneField(SeriesModel, on_delete=models.CASCADE, primary_key=True)
#     image = models.ImageField(upload_to='seasons/', null=True, blank=True)
#     trailer = models.CharField(max_length=5000, null=True, blank=True)
#     link1 = models.CharField(max_length=5000, null=True, blank=True)
#     link2 = models.CharField(max_length=5000, null=True, blank=True)
#     link3 = models.CharField(max_length=5000, null=True, blank=True)
#     online_link = models.CharField(max_length=5000, null=True, blank=True)
#     id = models.IntegerField(null=True, blank=True)
