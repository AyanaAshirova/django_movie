from django.core.files import File
import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movie
from utils.utils import get_video_duration, get_video_thumbnail
from .tasks import video_encode, save_recommended_movies, set_thumbnail
from .models import WatchList, VideoStream

@receiver(post_save, sender=Movie)
def save_recommendations(sender, instance, created, **kwargs):
    if not instance.recommendations.exists():
        save_recommended_movies.delay(5, instance.id)


@receiver(post_save, sender=VideoStream)
def add_thumbnail_and_video_duration(sender, instance, created, **kwargs):
    if instance:
        duration = get_video_duration(instance.video.path)
        if duration:
            instance.movie.duration = duration
            instance.movie.save(update_fields=['duration'])
        
        set_thumbnail.delay(3, instance.id)


@receiver(post_save, sender=VideoStream)
def start_encoding(sender, instance, created, **kwargs):
    if instance.status == VideoStream.PENDING:
        print('Signal triggered for encoding video:', instance.id)
        video_encode.delay(5,instance.id)


# @receiver(post_save, sender=Movie)
# def movie_signal(sender, instance, created, *args, **kwargs):
#     if created and instance:
#         video_encode.delay( 5, instance)
#         print("Task initiated")
#         try:
#             video_encode.delay(3,instance)
#         except Exception as e:
#             print("Celery error:", e)
    
            