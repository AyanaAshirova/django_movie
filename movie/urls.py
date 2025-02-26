from django.urls import path, include

from .views import *

urlpatterns = [
    path('/', HomePage.as_view(), name='home'),
    # path('categories/<category_id>/', views.categories, name='categories'),
    # path('movie_details/<movie_id>/', views.movie_details, name='movie_details'),
    # path('search_details/', views.search_details, name='search_details'),
]
