from django.db.models.signals import post_save
from django.dispatch import receiver
from movie.models import WatchList
from users.models import User
from .tasks import add_default_wachlists_to_user


@receiver(post_save, sender=User)
def create_defaultwatchlists(sender, instance, created, **kwargs):
    if created:
        add_default_wachlists_to_user(3, instance)