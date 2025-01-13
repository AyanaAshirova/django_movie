from datetime import datetime

from django.db import models



class Movie(models.Model):
    title = models.CharField(max_length=500)
    genres = models.ManyToManyField('Genre', related_name='movies')
    slug = models.SlugField(max_length=500)
    premium = models.BooleanField(default=False)
    discription = models.TextField(max_length=10000, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    thumbnail_link = models.CharField(max_length=1000, null=True, blank=True)
    background_image_link = models.CharField(max_length=1000, null=True, blank=True)
    screen_shot = models.ImageField(upload_to='screenshots/', null=True, blank=True)
    screen_shot_link = models.CharField(max_length=1000, null=True, blank=True)
    movie_length = models.CharField(max_length=50, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    movie_rate = models.CharField(max_length=100, null=True, blank=True)
    imdb_rating = models.CharField(max_length=100, null=True, blank=True)
    movie_director = models.CharField(max_length=200, null=True, blank=True)
    movie_actor = models.CharField(max_length=1000, null=True, blank=True)
    movie_language = models.CharField(max_length=100, null=True, blank=True)
    movie_subtitle = models.CharField(max_length=100, null=True, blank=True)
    movie_type = models.CharField(max_length=200, null=True, blank=True)
    movie_category = models.CharField(max_length=100, null=True, blank=True)
    link_4k = models.CharField(max_length=1000, null=True, blank=True)
    link_1920 = models.CharField(max_length=1000, null=True, blank=True)
    link_720 = models.CharField(max_length=1000, null=True, blank=True)
    size_4k = models.CharField(max_length=1000, null=True, blank=True)
    size_1920 = models.CharField(max_length=1000, null=True, blank=True)
    size_720 = models.CharField(max_length=1000, null=True, blank=True)
    movie_link = models.TextField(max_length=10000, null=True, blank=True)
    movie_online = models.TextField(max_length=1000, null=True, blank=True)
    torent_link_4k = models.CharField(max_length=1000, null=True, blank=True)
    torent_link_1920 = models.CharField(max_length=1000, null=True, blank=True)
    torent_link_720 = models.CharField(max_length=1000, null=True, blank=True)
    torent_file_link = models.FileField(upload_to='torent_movie', null=True, blank=True)

    tmvdbid = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.now)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def snippet(self):
        return self.discription[:10]+'...'

# ! Director, Actor, Sound, Subtitles,  Создатели:сценарист, Композитор, Оператор, Продюсер
class Person(models.Model):
    name = models.CharField(max_length=1000)
    photo = models.ImageField(upload_to='persons/')
    movies = models.ManyToManyField(Movie, related_name='movies')


class PersonRule(models.Model):
    name = models.CharField(max_length=1000)
    movies = models.ManyToManyField(Movie, related_name='movies')


class Genre(models.Model):
    name = models.CharField(max_length=75)
    tmvdbid = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


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


class MovieFrame(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='frames')
    frame_image = models.ImageField(upload_to='frames/')

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
