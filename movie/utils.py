from .models import *

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count


def get_popular_movie_set(queryset):
    result_movie_list = {}

    def _get_movies_by_period(date):
        return queryset.filter(views__created_at__gte=date)\
        .annotate(views_count=Count('views'))\
        .order_by('-views_count')

    def _add_movie_to_result(movie_list, label):
        for movie in movie_list:
            movie_id = movie.id
            if movie_id not in result_movie_list:    
                result_movie_list[movie_id] = {
                    'movie': movie,
                    'periods': set()
                }

            result_movie_list[movie_id]['periods'] .add(label)
        
    now = timezone.now()    
    today = now.date()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    year_ago = now - timedelta(days=365)

    popular_on_day = _get_movies_by_period(today)
    popular_in_week = _get_movies_by_period(week_ago)
    popular_for_month = _get_movies_by_period(month_ago)
    popular_for_year = _get_movies_by_period(year_ago)

    _add_movie_to_result(popular_on_day, 'day')
    _add_movie_to_result(popular_in_week, 'week')
    _add_movie_to_result(popular_for_month, 'month')
    _add_movie_to_result(popular_for_year, 'year')

    return result_movie_list


def add_views_to_movie(user, movie):
    movie.all_views += 1
    movie.save()

    if user.is_authenticated:
        MovieViews.objects.get_or_create(user=user, movie=movie)

