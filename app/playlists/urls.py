from django.urls import path
from .views import (
    ShowPlaylistsView,
    AddNewPlaylistView,
    EditPlaylistView,
    ShowPlaylistView,
    AddNewLinkView,
    like_ajax,
    dislike_ajax,
    remove_playlist_ajax,
    restore_playlist_ajax,
    inherite_ajax,
    check_alive_ajax,
    create_private_link_ajax,
    show_introduction_ajax
)


urlpatterns = [
    path(
        r"",
        ShowPlaylistsView.as_view(),
        name="show_playlists_n"
    ),
    path(
        r"playlist/new",
        AddNewPlaylistView.as_view(),
        name="add_new_playlist_n",
    ),
    path(
        r"playlist/<pk>/edit/",
        EditPlaylistView.as_view(),
        name="edit_playlist_n",
    ),
    path(
        r"playlist/<pk>",
        ShowPlaylistView.as_view(),
        name="show_playlist_n",
    ),
    path(
        r"playlist/",
        ShowPlaylistView.as_view(),
        name="show_playlist_n",
    ),
    path(
        r"playlist/<pk>/add_link/",
        AddNewLinkView.as_view(),
        name="add_new_link_n",
    ),
    path(
        r"ajax/like_playlist/<pk>",
        like_ajax,
        name="like_ajax_n"
    ),
    path(
        r"ajax/like_playlist/",
        like_ajax,
        name="like_ajax_n"
        ),
    path(
        r"ajax/dislike_playlist/<pk>",
        dislike_ajax,
        name="dislike_ajax_n"
    ),
    path(
        r"ajax/dislike_playlist/",
        dislike_ajax,
        name="dislike_ajax_n"
    ),
    path(
        r"ajax/remove_playlist/<pk>",
        remove_playlist_ajax,
        name="remove_playlist_n"
    ),
    path(
        r"ajax/restore_playlist/<pk>",
        restore_playlist_ajax,
        name="restore_playlist_n",
    ),
    path(
        r"ajax/inherite_playlist/<pk>",
        inherite_ajax,
        name="inherite_ajax_n"
    ),
    path(
        r"ajax/inherite_playlist/",
        inherite_ajax,
        name="inherite_ajax_n"
    ),
    path(
        r"ajax/check_alive/<pk>",
        check_alive_ajax,
        name="check_alive_ajax_n"
    ),
    path(
        r"ajax/check_alive/",
        check_alive_ajax,
        name="check_alive_ajax_n"
    ),
    path(
        r"ajax/create_private_link/<pk>",
        create_private_link_ajax,
        name="create_private_link_n"
    ),
    path(
        r"ajax/create_private_link/",
        create_private_link_ajax,
        name="create_private_link_n"
    ),
    path(
        r"ajax/intro_show/",
        show_introduction_ajax,
        name="show_intro_ajax_n"
    ),
]
