from django.urls import path
from .views import *

urlpatterns = [
    path("home/", HomeView.as_view(), name="home_n"),
    path("add_playlist/", AddNewPlaylistView.as_view(), name="add_new_playlist_n"),
    path("logout/", LogOutView, name="logout_n"),
]
