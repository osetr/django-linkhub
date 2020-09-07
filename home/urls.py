from django.urls import path
from .views import *

urlpatterns = [
    path("home/", HomeView.as_view(), name="home_n"),
    path("home/<target>/", HomeView.as_view(), name="home_target_n"),
    path("home/playlist/new", AddNewPlaylistView.as_view(), name="add_new_playlist_n"),
    path("home/playlist/show/<pk>", ShowPlaylistView.as_view(), name="show_playlist_n"),
    path("home/add_link/<pk>/", AddNewLinkView.as_view(), name="add_new_link_n"),
    path("logout/", LogOutView, name="logout_n"),
    path(r"^ajax/like_playlist/<pk>$", like_ajax, name="like_ajax_n"),
    path(r"^ajax/dislike_playlist/<pk>$", dislike_ajax, name="dislike_ajax_n"),
    path(r"^ajax/inherite_playlist/<pk>$", inherite_ajax, name="inherite_ajax_n"),
    path(r"^ajax/intro_show/$", show_introduction_ajax, name="show_intro_ajax_n"),
]
