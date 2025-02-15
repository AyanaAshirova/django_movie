from django.contrib import admin

from .models import *

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Person)
admin.site.register(Role)
admin.site.register(PersonRole)
admin.site.register(Purchase)
admin.site.register(Subscription)
admin.site.register(Raiting)

