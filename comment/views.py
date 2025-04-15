from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from movie.models import Movie
from .serializers import *
from .forms import AddCommentForm
from django.contrib.auth.models import User


from rest_framework.response import Response
from rest_framework import status

def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if not serializer.is_valid():
        print(serializer.errors)  # ← тут ты увидишь точную причину
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return super().create(request, *args, **kwargs)


class CommentApiView(generics.CreateAPIView):
    serializer_class = CommentSerializer(many=False)

class CommentListApiView(generics.ListAPIView):
    serializer_class = CommentApiView
    queryset = Comment.objects.all()


class CommentApiView(APIView):
    serializer_class = CommentApiView
    queryset = Comment.objects.all()


class MovieCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    
    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Comment.objects.filter(movie_id=movie_id).order_by('-created_at')

    def perform_create(self, serializer):
        movie_id = self.kwargs['movie_id']
        movie = generics.get_object_or_404(Movie, pk=movie_id)
        serializer.save(user=self.request.user, movie=movie, status=True)



@login_required
def add_comment(request, movie_id):
    reply_form = AddCommentForm()
    if request.method == 'POST':
        comment_form = AddCommentForm(request.POST)
        movie = Movie.objects.get(id=movie_id)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
            return redirect('movie_details', pk=movie_id)
    else:
        comment_form = AddCommentForm()
        return render(request, 'Comment/comment-form.html', {'form': comment_form, 'reply_form': reply_form, 'movie': movie})


@login_required
def reply_comment(request, movie_id, parent_id):
    if request.method == 'POST':
        comment_form = AddCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie_id = movie_id
            comment.user = request.user
            comment.parent_id = parent_id
            comment.save()
            return redirect('movie_details', pk=movie_id)
    else:
        comment_form = AddCommentForm()
        return render(request, 'Comment/reply-comment-form.html', {'reply_form': comment_form})



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