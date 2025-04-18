from django import template

from movie.models import Genre

register = template.Library()


@register.simple_tag
def get_genres():
    genres = Genre.objects.all()
    return genres