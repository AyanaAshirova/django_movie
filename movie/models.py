from datetime import datetime
from django.db import models
from django.core.validators import FileExtensionValidator
import os
from slugify import slugify
from utils.models import TimeStampAbstractModel
from django.conf import settings
from users.models import User


class Role(models.Model):
    name = models.CharField(max_length=55, verbose_name='Роль')

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=1000, verbose_name='Имя')
    photo = models.ImageField(upload_to=f'persons/{name}/', verbose_name='Фотографии', default='defaults/person.jpg')

    def __str__(self):
        return self.name


class MoviePerson(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='movie_person')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='movie_person', verbose_name='Человек')
    role = models.ForeignKey(Role, verbose_name='Роли', related_name='movie_person', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('person', 'movie', 'role')

    def __str__(self):
        return f'{self.person.name} - {self.movie.title}' 


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    

class Rating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]  # Создаем список (1, '1'), (2, '2'), ..., (10, '10')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Пользователь', related_name='ratings')
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='history')
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
    price = models.PositiveBigIntegerField(null=True, blank=True)
    poster = models.ImageField(upload_to='movies/posters/', blank=True, null=True, default='defaults/poster.jpg',)
    genres = models.ManyToManyField(Genre, verbose_name='Жанры', related_name='movie')
    description = models.TextField(max_length=10000, null=True, blank=True, verbose_name='Описание')
    duration = models.PositiveBigIntegerField(verbose_name='Длительность в секундах', blank=True, null=True)
    persons = models.ManyToManyField(Person, through=MoviePerson,verbose_name='Участники фильма')
    bg_photo = models.ImageField(upload_to='movies/bg_photos/',default='defaults/default-bg.jpg', blank=True, null=True)
    trailer_url = models.URLField(verbose_name='Ссылка на трейлер')

    recommendations = models.ManyToManyField('self', symmetrical=False, blank=True,)
    
    hls_master = models.CharField(max_length=500, blank=True, null=True, verbose_name='Путь к master.m3u8')

    # video_360 = models.FileField(
    #     upload_to='movies/videos/360/', 
    #     null=True, blank=True, 
    #     validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    # )
    # video_720 = models.FileField(
    #     upload_to='movies/videos/720/', 
    #     null=True, blank=True, 
    #     validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    # )
    # video_1920 = models.FileField(
    #     upload_to='movies/videos/1920/', 
    #     null=True, blank=True, 
    #     validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    # )
    # video_4k = models.FileField(
    #     upload_to='movies/videos/4k/', 
    #     null=True, blank=True, 
    #     validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    # )

    thumbnail = models.ImageField(upload_to='movies/thumbnail/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    all_views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=120, blank=True, unique=True)
    
    def get_duration_display(self):
        if self.duration:
            hours  = int(self.duration // 3600)
            min = int((self.duration % 3600) // 60)
            sec = int(self.duration % 60)
            return f'{hours}ч. {min}мин' if hours and min else f'{min}мин {sec}сек' if min and sec else f'{sec}сек'
        return 0

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.value for rating in ratings) / ratings.count(), 2)
        return 0

    def get_actors(self):
        return Person.objects.filter(movie_person__movie=self, movie_person__role__name='актёр')

    def get_creators(self):
        return Person.objects.filter(movie_person__movie=self).distinct()
    
    def get_recommended_movies(self):
        return Movie.objects\
            .filter(genres__in=self.genres.all())\
            .exclude(id=self.id).distinct()[:10]
    
        
    def generate_master_playlist(self):
        import os
        from .models import VideoStream
        movie_id = self.id


        base_dir = os.path.join(settings.MEDIA_ROOT, f'{settings.HLS_DIR_NAME}/{movie_id}')
        master_path = os.path.join(base_dir, 'master.m3u8')

        streams = VideoStream.objects.filter(movie_id=movie_id, status=VideoStream.COMPLETED)
        lines = ['#EXTM3U']

        for stream in streams:
            resolution = stream.resolution
            lines.append(f'#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x{resolution}')
            lines.append(f'{stream.resolution}/playlist.m3u8')

        with open(master_path, 'w') as f:
            f.write('\n'.join(lines))
        
        hls = f'media/{settings.HLS_DIR_NAME}/{movie_id}/master.m3u8'
        self.hls_master = hls
        self.save(update_fields=['hls_master'])
        
        return hls


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super (Movie, self).save(*args, **kwargs)

    def snippet(self):
        return self.description[:17]+'...'
    
    def __str__(self):
        return self.title
    
    def get_average_rating(self):
        from django.db.models import Avg
        result = Rating.objects\
                .filter(movie=self)\
                .aggregate(average_rating=Avg('value'))
        
        average_rating = result['average_rating']
                
        if average_rating is not None:
            average_rating = round(average_rating, 1)

        return average_rating
    

    
    

    
class VideoStream(TimeStampAbstractModel):
    movie = models.ForeignKey(Movie, related_name='streams', on_delete=models.CASCADE)

    resolution = models.CharField(
        max_length=10,
        choices=[
            ('360', '360'),
            ('480', '480'),
            ('720', '720'),
            ('1080', '1080')
        ]
    )

    video = models.FileField(upload_to='videos/')

    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    hls_path = models.CharField(max_length=500, blank=True, null=True)  # путь к master.m3u8
    is_running = models.BooleanField(default=False)

    @property
    def resolution_label(self):
        return f"{self.resolution}p"

    def __str__(self):
        return f"{self.movie.title} - {self.resolution}"



class WatchList(TimeStampAbstractModel):
    name = models.CharField(max_length=50, verbose_name='Название списка ')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlists')
    order = models.IntegerField(blank=True, null=True)

    FAVORITES = 'Любимые'
    WATCHED = 'Просмотренные'
    HISTORY = 'История'

    DEFAULT_WATCHLISTS = [
        FAVORITES,
        WATCHED,
        HISTORY
    ]

    # def save(self):
    #     if self.order is None:
    #         last_order = WatchList.objects.aggregate(models.Max('order'))['order_max']


class WatchListItem(TimeStampAbstractModel):
    watchlist = models.ForeignKey('WatchList', on_delete=models.CASCADE, related_name='items')
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlists_items')




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
