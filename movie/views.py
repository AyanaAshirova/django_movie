import random
from datetime import datetime
from django.db.models import Q

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from .models import *

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count


def get_popular_movie_set():
    result_movie_list = {}

    def _get_movies_by_period(date):
        return Movie.objects.filter(views__created_at__gte=date)\
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



class HomePage(TemplateView):
    template_name = 'Home/index.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['latest_movies'] = Movie.objects.all()[:6]
        context['top_views_movies'] = get_popular_movie_set()
        return context


class MovieDetail(DetailView):
    template_name = 'movie/anime-details.html'
    model = Movie

    def get_object(self, queryset = None):
        movie = super().get_object(queryset)
        user = self.request.user
        add_views_to_movie(user, movie)

        return movie


class MovieFilter(ListView):
    template_name = 'movie/categories.html'
    model = Movie

    def get_queryset(self):
        query_set = Movie.objects.all()
        filters = {}

        return query_set.filter(**filters).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')

        context['genre'] = Genre.objects.get(id=pk)
        context['movies'] = Movie.objects.filter(genres__id=pk).order_by('created_at')[:5]
        return context
    







