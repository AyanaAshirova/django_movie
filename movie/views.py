import random
from datetime import datetime
from django.db.models import Q

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.views import APIView
from .serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from .models import *
from .utils import get_popular_movie_set, add_views_to_movie


class HomePage(TemplateView):
    template_name = 'Home/index.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['latest_movies'] = Movie.objects.all()[:6]
        context['top_views_movies'] = get_popular_movie_set()
        return context


class MovieSearchApiView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        movies = Movie.objects.filter(title__incontains=query)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def movie_search(request):
    return render('movie/search-details.html')

class MovieDetail(DetailView):
    template_name = 'movie/anime-details.html'
    model = Movie

    def get_object(self, queryset = None):
        movie = super().get_object(queryset)
        user = self.request.user
        add_views_to_movie(user, movie)

        return movie
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["user"] = {
            "id": self.request.user.id,
            "username": self.request.user.username
            }
        return context
    


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
    







