from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from comment.views import CommentReplyView, MovieCommentListApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('comments/', include('comment.urls')),
    path('', include('movie.urls')),

    path('api/v1/movies/<int:movie_id>/comments/', MovieCommentListApiView.as_view(), name='movie-comments'),
    path('api/v1/comments/<pk>/reply', CommentReplyView.as_view()),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

