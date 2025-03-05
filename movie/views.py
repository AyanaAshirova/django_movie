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





