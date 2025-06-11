from rest_framework import serializers
from .models import Comment
from users.serializers import UserSerializer


    # user_id = serializers.IntegerField()
    # movie_id = serializers.IntegerField()
    # content = serializers.CharField()
    # parent_id = serializers.ImageField()
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'movie', 'content', 'parent', 'created_at']
        read_only_fields = ['id', 'created_at']

class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'movie', 'content', 'parent']
        read_only_fields = ['id', 'user']


