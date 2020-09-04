from django.urls import path
from .views import *

urlpatterns = [
    path("home/", HomeView.as_view(), name="home_n"),
    path("home/<target>/", HomeView.as_view(), name="home_target_n"),
    path("home/playlist/new", AddNewPlaylistView.as_view(), name="add_new_playlist_n"),
    path("home/add_link/<pk>/", AddNewLinkView.as_view(), name="add_new_link_n"),
    path("logout/", LogOutView, name="logout_n"),
]
