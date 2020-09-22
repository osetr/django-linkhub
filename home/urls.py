from django.urls import path
from .views import *

urlpatterns = [
    path("home/", HomeView.as_view(), name="home_n"),
    path("home/playlists/", ShowPlaylistsView.as_view(), name="show_playlists_n"),
    path(
        "home/playlists/playlist/new",
        AddNewPlaylistView.as_view(),
        name="add_new_playlist_n",
    ),
    path(
        "home/playlists/playlist/<pk>/edit/",
        EditPlaylistView.as_view(),
        name="edit_playlist_n",
    ),
    path(
        "home/playlists/playlist/<pk>/show/",
        ShowPlaylistView.as_view(),
        name="show_playlist_n",
    ),
    path(
        "home/playlists/playlist/<pk>/add_link/",
        AddNewLinkView.as_view(),
        name="add_new_link_n",
    ),
    path("logout/", LogOutView, name="logout_n"),
    path(r"^ajax/like_playlist/<pk>", like_ajax, name="like_ajax_n"),
    path(r"^ajax/like_playlist/", like_ajax, name="like_ajax_n"),
    path(r"^ajax/dislike_playlist/<pk>", dislike_ajax, name="dislike_ajax_n"),
    path(r"^ajax/dislike_playlist/", dislike_ajax, name="dislike_ajax_n"),
    path(
        r"^ajax/remove_playlist/<pk>$", remove_playlist_ajax, name="remove_playlist_n"
    ),
    path(
        r"^ajax/restore_playlist/<pk>$",
        restore_playlist_ajax,
        name="restore_playlist_n",
    ),
    path(r"^ajax/inherite_playlist/<pk>", inherite_ajax, name="inherite_ajax_n"),
    path(r"^ajax/inherite_playlist/", inherite_ajax, name="inherite_ajax_n"),
    path(r"^ajax/intro_show/$", show_introduction_ajax, name="show_intro_ajax_n"),
]
