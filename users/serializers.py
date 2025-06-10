from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'avatar', 'birth_date', 'username', 'last_login', 'date_joined']
        read_only_fields = ['id', 'date_joined']
