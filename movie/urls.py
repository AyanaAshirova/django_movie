from django.urls import path, include

from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('movie_details/<pk>/', MovieDetail.as_view(), name='movie_details'),
    path('movie_watching/<pk>/', HLSVideoPlayer.as_view(), name='movie_watching'),
    path('categories/<pk>/', MovieCategoryDetail.as_view(), name='categories'),
    path('filter/', MovieFilter.as_view(), name='filter'),
    path('person-details/<pk>/', PersonView.as_view(), name='person_details'),

]
