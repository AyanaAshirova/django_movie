from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from comment.views import CommentReplyView, MovieCommentListApiView, CommentView
from comment.views import *
# from movie.views import  MovieSearchApiView, serve_hls_playlist, serve_hls_segment, serve_hls_master, AddMovieToWatchList, RemoveMovieFromWatchList, UserMovieWatchListApiView, WatchListApiView, RatingApiView
from movie.views import  *
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('users.urls')),

    path('comments/', include('comment.urls')),
    path('', include('movie.urls')),
    

    path('api/v1/movies/<int:movie_id>/comments/', MovieCommentListApiView.as_view(), name='movie-comments'),
    path('api/v1/comments/<int:parent_id>/reply/', CommentReplyView.as_view()),
    path('api/v1/comments/', CommentView.as_view()),
    
    path('api/v1/movies/search/<str:query>', MovieSearchApiView.as_view()),
    path('api/v1/movies/<int:movie_id>/rating/average/', RatingApiView.as_view()),

    path('api/v1/users/<int:user_id>/watchlists/', WatchListApiView.as_view()),
    path('api/v1/users/movies/<int:movie_id>/rating/', UserRatingApiView.as_view()),

    path('api/v1/persons/<int:person_id>/roles/<int:role_id>/movies/', PersonRoleMoviesApiView.as_view()),
    path('api/v1/persons/<int:person_id>/roles/', PersonRolesApiView.as_view()),


    path('api/v1/watchlists/movies/<int:movie_id>/add_to_watchlist/<int:list_id>/', AddMovieToWatchList.as_view(), name='add_to_watchlist'),
    path('api/v1/watchlists/movies/<int:movie_id>/remove_from_watchlist/', RemoveMovieFromWatchList.as_view(), name='remove_from_watchlists'),
    path('api/v1/watchlists/users/<int:user_id>/movies/<int:movie_id>/', UserMovieInWatchListApiView.as_view()),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

