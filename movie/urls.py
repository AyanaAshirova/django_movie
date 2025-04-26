from django.urls import path, include

from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('movie_details/<pk>/', MovieDetail.as_view(), name='movie_details'),
    path('categories/<pk>/', MovieCategoryDetail.as_view(), name='categories'),
    path('movie_search/', movie_search, name='movie_search'),
]
