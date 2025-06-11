from celery import shared_task
from movie.models import WatchList
from time import sleep

@shared_task
def add_default_wachlists_to_user(duration, user):
    sleep(duration)
    for name in WatchList.DEFAULT_WATCHLISTS:
        WatchList.objects.get_or_create(name=name, user=user)