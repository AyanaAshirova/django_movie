from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from movie.models import Movie
from .serializers import *
from .forms import AddCommentForm
from django.contrib.auth.models import User


from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status


class MovieCommentListApiView(APIView):
    def get(self, request, movie_id):
        comments = Comment.objects.filter(movie__id=movie_id).order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    # serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    
    # def get_queryset(self):
    #     movie_id = self.kwargs['movie_id']
    #     return Comment.objects.filter(movie_id=movie_id).order_by('-created_at')

    # def perform_create(self, serializer):
    #     movie_id = self.kwargs['movie_id']
    #     movie = generics.get_object_or_404(Movie, pk=movie_id)
    #     serializer.save(user=self.request.user, movie=movie, status=True)


class CommentReplyView(APIView):
    def post(self, request, pk):
        try:
            Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'error': 'Parent Comment does not exists'}, status=status.HTTP_404_NOT_FOUND)
        
        reply_data = request.data
        serializer = CommentSerializer(data=reply_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# @login_required
# def like_comment(request, comment_id, movie_id):
#     comment = get_object_or_404(Comment, id=comment_id)
#     like, created = CommentLikes.objects.get_or_created(user=request.user, comment=comment)
#
#     if not created:
#         like.delete()
#     return redirect('movie_details', movie_id=movie_id)



    # if request.method == 'POST':
    #     query = request.GET.get('reaction', '')
    #     # srch = movie_api.search(query)
    #
    #     context = {
    #         'query': query
    #     }
    #     return render(request, 'Movies/search-details.html', context)