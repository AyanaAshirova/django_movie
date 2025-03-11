from django.urls import path, include

from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('movie_details/<pk>/', MovieDetail.as_view(), name='movie_details'),
    path('categories/<pk>/', MovieFilter.as_view(), name='categories'),
    # path('search_details/', views.search_details, name='search_details'),
]
