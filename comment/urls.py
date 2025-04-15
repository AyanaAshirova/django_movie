from django.urls import path

from .views import *

urlpatterns = [
    path('add_comment/<int:movie_id>', add_comment, name='add_comment'),
    path('reply_comment/<int:movie_id>/<int:parent_id>',reply_comment, name='reply_comment'),
    # path('like_comment/<comment_id><movie_id>', like_comment, name='like_comment'),
]