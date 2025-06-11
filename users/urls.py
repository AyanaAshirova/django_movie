from django.urls import path, include
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout', ),
]
