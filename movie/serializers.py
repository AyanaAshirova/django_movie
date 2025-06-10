
from rest_framework import serializers
from .models import Movie, Genre, Country, WatchList, WatchListItem, Rating, Role, MoviePerson, Person


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True) 
    country = CountrySerializer() 
    user_rating = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField()
    views = serializers.IntegerField(source='views.count', read_only=True)
    comments = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_date', 'country', 'poster', 'genres', 'bg_photo', 'created_at', 'slug', 'all_views', 'views', 'user_rating', 'average_rating', 'comments']
        read_only_fields = ['id', 'views', 'user_rating', 'average_rating', 'comments']

    
    def get_user_rating(self, instance):
        request =  self.context.get('request')
        if request:
            user = request.user
            if user.is_authenticated: 
                rating  = Rating.objects.filter(movie=instance, user=user).first()
                return rating.value if rating else None
        else:
            return None
    
    def get_average_rating(self, instance):
        from .utils import get_average_rating
        return get_average_rating(instance.id)



class WatchListItemSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()

    class Meta:
        model = WatchListItem
        fields = ['id', 'movie', 'created_at', 'updated_at']

    def get_movie(self, instance):
        serializer = MovieSerializer(instance.movie, context={'request': self.context['request']})
        return serializer.data



class WatchListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model =  WatchList
        fields = ['id', 'name', 'user', 'order', 'items']

    def get_items(self, instance):
        serializer = WatchListItemSerializer(instance.items, many=True, context={'request': self.context['request']})
        return serializer.data
    


class UserMovieWatchListSerializer(serializers.ModelSerializer):
    movie_is_watchlist = serializers.SerializerMethodField()
    class Meta:
        model = WatchList
        fields = ['id', 'created_at', 'updated_at', 'name', 'order', 'user', 'movie_is_watchlist']

    def get_movie_is_watchlist(self, instance):
        movie_id = self.context['movie_id']

        for item in instance.items.all():
            if item.movie.id == movie_id:
                return True
        return False


class PostRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['movie', 'value']


    def create(self, validated_data):
        return Rating.objects.create(**validated_data)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user','movie', 'value']
        read_only_fields = ['user']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']
