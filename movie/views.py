import random
from datetime import datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView

from .models import *


class HomePage(TemplateView):
    template_name = 'Home/index.html'

    def get_context_data(self, **kwargs):
        contex =  super().get_context_data(**kwargs)
        
        contex['latest_movies'] = Movie.objects.all()[:6]
        return contex


class MovieDetail(DetailView):
    template_name = 'movie/anime-details.html'
    model = Movie

    def get_object(self, queryset = None):
        movie = super().get_object(queryset)
        user = self.request.user
        # movie.all_views += 1
        if user.is_authenticated:
            MovieViews.objects.get_or_create(user=user, movie=movie)

        return movie


class MovieFilter(ListView):
    template_name = 'movie/catagories.html'
    model = Movie

    def get_queryset(self):
        query_set = Movie.objects.all()
        filters = {}

        return query_set.filter(**filters).distinct()







