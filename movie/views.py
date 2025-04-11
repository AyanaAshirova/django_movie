import random
from datetime import datetime

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

    def _add_movie_to_result(movie_list, label):
        for movie in movie_list:
            id = movie['id']
            print(id)
            # result_movie_list[id] = {
            #     'movie': movie,
            #     'periods': set(result_movie_list[id]['periods']).add(label)
            # }

        
    today = timezone.now().date()
    week_ago = timezone.now() - timedelta(days=7)
    month_ago = timezone.now() - timedelta(days=30)

    popular_on_day = Movie.objects.filter(views__created_at_date__gte=today)\
        .annotate(views_count=Count('views'))\
        .order_by('-views_count')
    popular_in_week = Movie.objects.filter(views__created_at_date__gte=week_ago)\
        .annotate(views_count=Count('views'))\
        .order_by('-views_count')
    popular_for_month = (
        Movie.objects.filter(views__created_at_date__gte=month_ago)
        .annotate(views_count=Count('views'))
        .order_by('-views_count')
        )
    _add_movie_to_result(popular_on_day, 'day')
    _add_movie_to_result(popular_in_week, 'week')
    _add_movie_to_result(popular_for_month, 'month')

    return result_movie_list



class HomePage(TemplateView):
    template_name = 'Home/index.html'
    a = get_popular_movie_set()
    print(a)

    def get_context_data(self, **kwargs):
        contex =  super().get_context_data(**kwargs)
        contex['latest_movies'] = Movie.objects.all()[:6]

        

        contex['top_views_movies'] = Movie.objects.order_by('views')[:6]
        return contex


class MovieDetail(DetailView):
    template_name = 'movie/anime-details.html'
    model = Movie

    def get_object(self, queryset = None):
        movie = super().get_object(queryset)
        user = self.request.user
        movie.all_views += 1
        if user.is_authenticated:
            MovieViews.objects.get_or_create(user=user, movie=movie)

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
    







