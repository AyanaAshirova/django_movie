from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import User
from movie.models import WatchList, WatchListItem, Rating
from movie.serializers import WatchListSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from movie.serializers import PostRatingSerializer, RatingSerializer


class UserProfileView(TemplateView):
    template_name = 'account/profile.html'

class UserRatingApiView(APIView):
    def post(self, request, movie_id):
        if request.user.is_authenticated:
            ratind_data = request.data
            serializer = PostRatingSerializer(data=ratind_data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, movie_id):
        try:
            rating = get_object_or_404(Rating, user=request.user, movie__id=movie_id)
            rating.delete()
            return Response({'detail': 'Rating deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'detail': 'Rating not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, movie_id):
        user = request.user
        rating = get_object_or_404(Rating, user=user, movie__id=movie_id)
        serializer = RatingSerializer(rating)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    

    