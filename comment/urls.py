from django.urls import path

from . import views

urlpatterns = [
    path('add_comment/<int:movie_id>', views.add_comment, name='add_comment'),
    path('reply_comment/<int:movie_id>/<int:parent_id>', views.reply_comment, name='reply_comment'),

    # path('like_comment/<comment_id><movie_id>', views.like_comment, name='like_comment'),
]