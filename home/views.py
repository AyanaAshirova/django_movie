import os
from datetime import datetime

from django.db.models import Count
from django.shortcuts import render
from Movies.models import Genre, Movies
from tmdbv3api import TMDb, Movie
import pandas as pd
from slugify import slugify
import numpy as np

from Comment.models import Comment

from Account.models import Profile

apikey = os.getenv('TMDB_API_KEY')
# apikey = '9fa12374bfa1ee4104add97410cc9f5c'
img_pre_path = 'http://image.tmdb.org/t/p/original'
default_poster = 'posters/default.jpg'


def MainHome(request):
    user = request.user
    categories = Genre.objects.all()
    movies = Movies.objects.annotate(num_comments=Count('comments'))

    tmdb = TMDb()
    tmdb.language = 'en_En'
    tmdb.api_key = apikey
    movie_api = Movie()

    latest_movies = []
    latest_movies_model = movies.order_by('-release_date')[:9]
    for i in latest_movies_model:
        genre_obj = i.genres.values_list('name', flat=True)
        i.genre_list = genre_obj
        details = movie_api.details(i.tmvdbid)
        i.poster_path = default_poster
        if details.poster_path:
            i.poster_path = img_pre_path + details.poster_path

        i.tmdb = details
        latest_movies.append(i)

    popular_movies = []
    popular_movies_model = movies.order_by('-views')[:9]
    for i in popular_movies_model:
        genre_obj = i.genres.values_list('name', flat=True)
        i.genre_list = genre_obj
        details = movie_api.details(i.tmvdbid)
        i.poster_path = default_poster
        if details.poster_path:
            i.poster_path = img_pre_path + details.poster_path

        i.tmdb = details
        popular_movies.append(i)

    top_raited = []
    top_raited_obj = movie_api.top_rated()
    # for i in top_raited_obj:
    #     i.comments_count = 0
    #     if movies.filter(tmvdbid=i.id).exists():
    #         movie = movies.get(tmvdbid=i.id)
    #         comments = comments.filter(movie=movie)
    #         i.comments_count = len(comments)
    #     popular_movie.append(i)

    hero_movies = []

    new_comments = []
    new_comments_model = Comment.objects.order_by('-created_at')[:6]
    for i in new_comments_model:
        if i.movie in [c.movie for c in new_comments]:
            continue
        genre_obj = i.movie.genres.values_list('name', flat=True)
        i.movie.genre_list = genre_obj
        details = movie_api.details(i.movie.tmvdbid)
        i.movie.poster_path = default_poster
        if details.poster_path:
            i.poster_path = img_pre_path + details.poster_path

        i.movie.tmdb = details
        new_comments.append(i)

    j = 0
    for i in popular_movies:
        if j >= 4:
            break
        i.tmdb.overview = i.tmdb.overview[:60] + '...'
        i.backdrop_path = default_poster
        if i.tmdb.backdrop_path:
            i.backdrop_path = img_pre_path + i.tmdb.backdrop_path

        hero_movies.append(i)
        j += 1

    contex = {
        'user': user,
        'categories': categories,
        'latest_movies': latest_movies,
        'popular_movies': popular_movies,
        'top_raited': top_raited,
        'hero_movies': hero_movies,
        'new_comments': new_comments,

    }
    return render(request, 'HomeApp/MainHome.html', contex)



