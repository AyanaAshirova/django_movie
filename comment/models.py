from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from Movies.models import Movies


class Comment(models.Model):
    content = models.CharField(max_length=3000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comments')
    movie = models.ForeignKey(Movies, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.movie.name} : "{self.created_at}"'


# class CommentLikes(models.Model):
#     user = models.ForeignKey(User, related_name='comment_likes', on_delete=models.CASCADE)
#     comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE)
#     date = models.DateTimeField(default=timezone.now)
#     islike = models.BooleanField(default=True)
#
#     class Meta:
#         unique_together = ('user', 'comment')
#
