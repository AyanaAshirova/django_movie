from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from comment.models import Comment
from movie.models import Movie
from rest_framework.pagination import PageNumberPagination


class DataMixin:
    paginate_by = 12

    def get_queryset(self):
        return Movie.objects.all()
    
    def get_ordering(self):
        ordering = self.request.GET.get('sort', 'title')  
        allowed = ['title', '-title', 'release_date', '-release_date', 'rating', '-rating']
        return ordering if ordering in allowed else 'title'
     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
  
        context['top_views_movies'] = get_popular_movie_set(self.get_queryset())
        
        recent_comments = Comment.objects\
            .select_related('movie')\
            .order_by('-created_at')\
            
        seen_movies = []
        unique_comments = []
        for comment in recent_comments:
            if comment.movie.id not in seen_movies:
                seen_movies.append(comment.movie.id)
                unique_comments.append(comment)
            if len(unique_comments) >= 10:
                break

        context['latest_comments'] = unique_comments
        return context


def get_popular_movie_set(queryset):
    result_movie_list = {}

    def _get_movies_by_period(date):
        return queryset.filter(views__created_at__gte=date)\
        .annotate(views_count=Count('views'))\
        .order_by('-views_count')

    def _add_movie_to_result(movie_list, label):
        for movie in movie_list:
            if movie.id not in result_movie_list:  
                result_movie_list[movie.id] = {
                    'movie': movie,
                    'periods': set()
                }

            result_movie_list[movie.id]['periods'].add(label)
        
    now = timezone.now()    
    today = now.date()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    year_ago = now - timedelta(days=365)

    popular_on_day = _get_movies_by_period(today)
    popular_in_week = _get_movies_by_period(week_ago)
    popular_for_month = _get_movies_by_period(month_ago)
    popular_for_year = _get_movies_by_period(year_ago)

    _add_movie_to_result(popular_on_day, 'day')
    _add_movie_to_result(popular_in_week, 'week')
    _add_movie_to_result(popular_for_month, 'month')
    _add_movie_to_result(popular_for_year, 'year')

    return result_movie_list


def add_views_to_movie(user, movie):
    from movie.models import MovieViews

    movie.all_views += 1
    movie.save()

    if user.is_authenticated:
        MovieViews.objects.get_or_create(user=user, movie=movie)


def remove_movie_from_user_watchlists(user_id, movie_id):
    from movie.models import WatchListItem, WatchList
    items = WatchListItem.objects\
        .filter(user=user_id, movie=movie_id)\
        .exclude(watchlist__name=WatchList.HISTORY)
    del_items = []
    if items.exists():
        for item in items:
            print(item.watchlist.name)
            if item:
                del_items.append(item.watchlist.name)
                item.delete()

    return del_items

def get_average_rating(movie_id):
    from django.db.models import Avg
    from movie.models import Rating
    result = Rating.objects\
            .filter(movie__id=movie_id)\
            .aggregate(average_rating=Avg('value'))
    
    average_rating = result['average_rating']
            
    if average_rating is not None:
        average_rating = round(average_rating, 1)

    return average_rating

def add_user_rating_to_movie_queryset(request, queryset):
    from movie.models import Rating
    if request:
        user = request.user
        for m in queryset:
            m.user_rating = None
            if request.user.is_authenticated:
                rating = Rating.objects.filter(movie=m, user=user).first()
                if rating:
                    m.user_rating = rating.value
                    continue

    return queryset
