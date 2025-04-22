from rest_framework import serializers
from .models import Comment


    # user_id = serializers.IntegerField()
    # movie_id = serializers.IntegerField()
    # content = serializers.CharField()
    # parent_id = serializers.ImageField()
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'movie', 'content', 'parent', 'created_at')
        read_only_fields = ('username', 'created_at')

