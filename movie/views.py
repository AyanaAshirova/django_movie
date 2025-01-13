import random
from datetime import datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import os
from django.shortcuts import render, redirect, get_object_or_404
from slugify import slugify
from django.utils import timezone
from tmdbv3api import TMDb, Movie
from .models import Movies
from .models import Genre
from Comment.models import Comment
from Account.models import Profile

from tpblite import TPB

# apikey = '9fa12374bfa1ee4104add97410cc9f5c'
apikey = os.getenv('TMDB_API_KEY')

tpb = TPB('https://tpb.party')
tmdb = TMDb()
tmdb.api_key = apikey
movie_api = Movie()


img_pre_path = 'http://image.tmdb.org/t/p/original'
default_poster = 'posters/default.jpg'


def movie_details(request, movie_id):
    user = request.user
    movie_obj = get_object_or_404(Movies, id=movie_id)
    movie_obj.views += 1
    movie_obj.save()

    tmdb_details = movie_api.details(movie_obj.tmvdbid)
    tmdb.language = 'en-En'
    torrents = tpb.search(tmdb_details.original_title)

    tmdb_details.runtime = f'{tmdb_details.runtime // 60}, {tmdb_details.runtime % 60} h.'
    tmdb_recommendations = movie_api.recommendations(movie_obj.tmvdbid)
    names = movie_api.alternative_titles(movie_obj.tmvdbid)

    comments = movie_obj.comments.all().filter(parent__isnull=True)

    contex = {
        'movie': movie_obj,
        'tmdbd': tmdb_details,
        'tmdbr': tmdb_recommendations,
        'alt_names': names,
        'torrents': torrents,
        'comments': comments,
    }

    return render(request, 'Movies/anime-details.html', contex)


def search_details(request):
    if request.method == 'GET':
        query = request.GET.get('searchinput', '')
        # srch = movie_api.search(query)
        srch = []
        movies = None
        if query:
            movies = Movies.objects.filter(name__icontains=query)

        if movies:
            for i in movies:
                genre_obj = i.genres.values_list('name', flat=True)
                i.genre_list = genre_obj
                details = movie_api.details(i.tmvdbid)
                i.poster_path = default_poster
                if details.poster_path:
                    i.poster_path = img_pre_path + details.poster_path

                i.tmdb = details
                srch.append(i)

        context = {
            'search_res': srch,
            'query': query
        }
        return render(request, 'Movies/search-details.html', context)


def categories(request, category_id):
    genre = Genre.objects.get(id=category_id)
    movies = genre.movies.order_by('-views')[:12]
    result = []

    for i in movies:
        genre_obj = i.genres.values_list('name', flat=True)
        i.genre_list = genre_obj
        details = movie_api.details(i.tmvdbid)
        i.poster_path = default_poster
        if details.poster_path:
            i.poster_path = img_pre_path + details.poster_path

        i.tmdb = details
        result.append(i)

    context = {
        'genre': genre,
        'movies': result
    }

    return render(request, 'Movies/categories.html', context)
