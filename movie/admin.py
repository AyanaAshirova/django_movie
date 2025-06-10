from django.contrib import admin
from .models import *


class VideoStreamAdmin(admin.ModelAdmin):
    list_display = ('movie', 'resolution', 'is_running', 'status')

class WatchListItemInline(admin.TabularInline):
    model = WatchListItem
    extra = 1

class WatchListAdmin(admin.ModelAdmin):
    inlines = [WatchListItemInline]



admin.site.register(VideoStream, VideoStreamAdmin)
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Person)
admin.site.register(Role)
admin.site.register(MoviePerson)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(Rating)

