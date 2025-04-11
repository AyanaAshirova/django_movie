from datetime import datetime
from django.db import models
from django.core.validators import FileExtensionValidator
import os
from slugify import slugify
from django.contrib.auth.models import User


class Role(models.Model):
    name = models.CharField(max_length=55, verbose_name='Роль')

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=1000, verbose_name='Имя')
    photo = models.ImageField(upload_to=f'persons/{name}/', verbose_name='Фотографии')

    def __str__(self):
        return self.name


class MoviePerson(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='movie_persons')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='movie_roles', verbose_name='Человек')
    role = models.ForeignKey(Role, verbose_name='Роли', related_name='movie_roles', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('person', 'movie', 'role')


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    

class Rating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]  # Создаем список (1, '1'), (2, '2'), ..., (10, '10')

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Пользователь', related_name='ratings')
    movie = models.ForeignKey('Movie', on_delete=models.DO_NOTHING, related_name='ratings', verbose_name='Фильм')
    value = models.IntegerField(choices=RATING_CHOICES, verbose_name='Оценка')

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.user} - {self.movie} : {self.value}'


class MovieFrame(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='frames')
    image = models.ImageField(upload_to='movie/frames/')


class MovieViews(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='history')
    movie = models.ForeignKey('Movie', on_delete=models.DO_NOTHING, related_name='views')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    release_date = models.DateField(verbose_name='Дата выхода')
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, related_name='movies')
    premium = models.BooleanField(default=False)
    price = models.PositiveBigIntegerField(null=True)
    poster = models.ImageField(upload_to='movies/posters/', blank=True, null=True, default='movies/default-poster.jpg',)
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    description = models.TextField(max_length=10000, null=True, blank=True, verbose_name='Описание')
    movie_length = models.PositiveBigIntegerField(verbose_name='Длительность в минутах')
    persons = models.ManyToManyField(Person, through=MoviePerson,verbose_name='Участники фильма')
    bg_photo = models.ImageField(upload_to='movies/bg_photos/',default='movies/default-bg.jpg', blank=True, null=True)
    trailer_url = models.URLField(verbose_name='Ссылка на трейлер')

    video_360 = models.FileField(
        upload_to='movies/videos/360/', 
        null=True, blank=True, 
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
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
    all_views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=120, blank=True, unique=True)

    def get_duration_display(self):
        hours = self.movie_length // 60
        min = self.movie_length % 60
        return f'{hours}ч. {min}мин' if hours else f'{min}мин'

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.value for rating in ratings) / ratings.count(), 2)
        return 0

    def get_actors(self):
        return Person.objects.filter(movie_roles__movie=self, movie_roles__role__name='актёр')

    def get_creators(self):
        return Person.objects.filter(movie_roles__movie=self).distinct()

    def __str__(self):
        return f'{self.title} - {self.release_date}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super (Movie, self).save(*args, **kwargs)

    def snippet(self):
        return self.description[:17]+'...'
    


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription', verbose_name='Пользователь')
    start_date = models.DateField(auto_now_add=True, verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')


class Purchase(models.Model):
    user = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,related_name='purchases', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')

    class Meta:
        unique_together = ('user', 'movie')








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
