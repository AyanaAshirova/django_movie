import random
from datetime import datetime
from django.db.models import Q, Avg, Count
from django.contrib.postgres.search import SearchVector
import os

from typing import Any
from django.db.models.query import QuerySet

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
# from .serializers import MovieSerializer, UserMovieWatchListSerializer, WatchListSerializer, PostRatingSerializer
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File

from movie.utils import  *
from utils.utils import get_video_duration, get_video_thumbnail

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from .models import *
from comment.models import Comment
from django.http import FileResponse, HttpResponse
from django.urls import reverse
from .tasks import video_encode
from django.contrib.auth.decorators import login_required
from django.conf import settings



class HLSVideoPlayer(DetailView):
    template_name = 'movie/anime-watching.html'
    model = Movie
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        movie = Movie.objects.get(id=self.kwargs.get('pk'))
        # context['hls_url'] = reverse('serve_hls_playlist', args=[movie.id])
        if not movie.hls_master: 
            movie.generate_master_playlist()
        context['hls_master_url'] = f'{settings.MEDIA_URL}{movie.hls_master}'
        if self.request.user.is_authenticated:
            watchlist, created = WatchList.objects.get_or_create(user=self.request.user, name=WatchList.HISTORY)
            WatchListItem.objects.get_or_create(movie=movie, user=self.request.user, watchlist=watchlist)

        return context
    

class MovieDetail(DetailView):
    template_name = 'movie/anime-details.html'
    model = Movie

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        movie = Movie.objects.get(id=self.kwargs.get('pk'))

        add_views_to_movie(self.request.user, movie)
        context['is_video'] = movie.streams.exists()
        movie.average_rating = get_average_rating(movie.id)
        context['recommendations'] = add_user_rating_to_movie_queryset(self.request, movie.recommendations.all())
        
        return context


class PersonView(DataMixin, ListView):
    template_name = 'movie/person-details.html'
    model = Movie

    def get_queryset(self):
        queryset =  super().get_queryset()
        person = get_object_or_404(Person, id=self.kwargs.get('pk'))
        queryset = queryset.filter(movie_person__person=person).distinct().annotate(average_rating=Avg('ratings__value'))
        queryset = add_user_rating_to_movie_queryset(self.request, queryset)
        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        person = get_object_or_404(Person, id=self.kwargs.get('pk'))

        context['person'] = person
        context['genres'] = Genre.objects.filter(movie__movie_person__person=person).distinct()
        context['movies_count'] = Movie.objects.filter(movie_person__person=person).count()
        context['countries'] = Country.objects.filter(movies__movie_person__person=person).distinct()
        context['roles'] = Role.objects.filter(movie_person__person=person)

        return context



class HomePage(DataMixin ,TemplateView):
    template_name = 'Home/index.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        latest_movies = Movie.objects.all().order_by('-all_views')[:12]
        latest_movies = add_user_rating_to_movie_queryset(self.request, latest_movies)

        context['latest_movies'] = latest_movies
            
        return context


class MovieSearchApiView(APIView):
    def get(self, request, query):
        movies = Movie.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        # movies = Movie.objects.annotate(
        #     search=SearchVector('title', 'description')
        # ).filter(search=query)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MovieFilter(DataMixin, ListView):
    template_name = 'movie/filter-page.html'
    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['countries'] = Country.objects.all()
        return context

    def get_queryset(self):
        queryset =  super().get_queryset()
        filters = {}
        genres = self.request.GET.get('genres')
        countries = self.request.GET.getlist('countries')

        if genres:
            filters['genres__id__in'] = genres

        if countries:
            filters['country__id__in'] = countries

        queryset = queryset.filter(**filters).distinct().annotate(average_rating=Avg('ratings__value'))

        queryset = add_user_rating_to_movie_queryset(self.request, queryset)

        return queryset
    

class MovieCategoryDetail(DataMixin, ListView):
    template_name = 'movie/categories.html'
    model = Movie
    
    def get_queryset(self) -> QuerySet[Any]:
        pk = self.kwargs.get('pk')
        return Movie.objects.filter(genres__id=pk).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['genre'] = Genre.objects.get(id=pk)

        return context
    

class RatingApiView(APIView):
    def get(self, request, movie_id):
        average_rating = get_average_rating(movie_id=movie_id)
        count = Rating.objects\
            .filter(movie__id=movie_id)\
            .count()
        
        return Response({"average_rating": average_rating, "count": count}, status.HTTP_200_OK)



class WatchListApiView(APIView):
    def get(self, request, user_id):
        watchlists = WatchList.objects.filter(user__id=user_id)
        serializer = WatchListSerializer(watchlists, many=True, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)




class UserMovieInWatchListApiView(APIView):
    def get(self, request, user_id, movie_id):
        watchlists = WatchList.objects.filter(user__id=user_id)

        serializer = UserMovieWatchListSerializer(watchlists,context = {'movie_id': movie_id}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AddMovieToWatchList(APIView):
    def post(self, request, movie_id, list_id):
        user = get_object_or_404(User,id=request.user.id)
        if request.user.is_authenticated:
            movie = get_object_or_404(Movie, id=movie_id)
            watchlist = get_object_or_404(WatchList, id=list_id)
            del_items = remove_movie_from_user_watchlists(user_id=user.id, movie_id=movie_id)
            _, created = WatchListItem.objects.get_or_create(watchlist=watchlist, movie=movie, user=user)

            if created:
                return Response({'status': f'Added to watclist "{watchlist.name}", delete from {del_items}'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Movie already in watchlist'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


class RemoveMovieFromWatchList(APIView):
    def post(self, request, movie_id):
        user = get_object_or_404(User, id=request.user.id)
        if request.user.is_authenticated:
            movie = get_object_or_404(Movie, id=movie_id)
            del_items = remove_movie_from_user_watchlists(user_id=user.id, movie_id=movie_id)
            if len(del_items) > 0:
                return Response({'status': f'Movie removed from watchlist {del_items}'}, status=status.HTTP_200_OK)
            return Response({'status': 'Movie is not in watchlists'}, status=status.HTTP_404_NOT_FOUND)
            
        
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


class PersonRoleMoviesApiView(ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        person_id = self.kwargs.get('person_id')
        role_id = self.kwargs.get('role_id')
        return Movie.objects.filter(
            movie_person__person__id=person_id,
            movie_person__role__id=role_id
        )



class PersonRolesApiView(APIView):
    def get(self, request, person_id):
        try:
            person = get_object_or_404(Person, id=person_id)
            roles = Role.objects.filter(movie_person__person=person)
            roles_serializer = RoleSerializer(roles, many=True)

            return Response(roles_serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response('Person not found', status=status.HTTP_404_NOT_FOUND)




