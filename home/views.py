from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Playlist
from .forms import AddNewPlaylistForm, AddNewLinkForm
from django.http import JsonResponse, HttpResponse
import re


class HomeView(View):
    def get(self, request, target="main"):
        user_authenticated = request.user.is_authenticated
        if target == "main":
            return render(
                request,
                "home.html",
                context={"user_authenticated": user_authenticated, 
                        "active_page": "home",
                        "target": target},
            )
        elif target == "personal_playlists":
            playlists = list(Playlist.objects.filter(author=request.user.id).values())
            if not playlists:
                page_header = "Nothing found"
                playlists = "List is empty"
            else:
                page_header = "Playlist's list"
            return render(
                request,
                "home.html",
                context={
                    "user_authenticated": user_authenticated,
                    "active_page": "home",
                    "page_header": page_header,
                    "playlists": playlists,
                    "target": target,
                },
        )
        else:
            return redirect('home_target_n', target="main")

    def post(self, request, target="search_playlists"):
        user_authenticated = request.user.is_authenticated
        playlists_keys = request.POST.get("playlists_keys", "")
        playlists = list(Playlist.objects.values())

        def amount_of_occurences(str):
            general_amount = 0
            for key in playlists_keys.split():
                general_amount += len(re.findall(key, str["title"]))
                general_amount += len(re.findall(key, str["description"]))
            return general_amount

        playlists.sort(
            key=lambda a: (amount_of_occurences(a), int(a["likes"])), 
            reverse=True
        )
        if not playlists:
            page_header = "Nothing found"
            playlists = "List is empty"
        else:
            page_header = "Playlist's list"
        return render(
            request,
            "home.html",
            context={
                "user_authenticated": user_authenticated,
                "active_page": "home",
                "page_header": page_header,
                "playlists": playlists,
                "target": target,
            },
        )


class AddNewPlaylistView(View):
    def get(self, request):
        form = AddNewPlaylistForm()
        user_authenticated = request.user.is_authenticated

        return render(
            request,
            "add_playlist.html",
            context={"user_authenticated": user_authenticated,
                     "form": form}
        )

    def post(self, request):
        form = AddNewPlaylistForm(request.POST)
        user_authenticated = request.user.is_authenticated

        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.author = request.user
            playlist.save()
        return redirect("home_n")


class AddNewLinkView(View):
    def get(self, request, pk):
        form = AddNewLinkForm()
        user_authenticated = request.user.is_authenticated

        return render(
            request,
            "add_link.html",
            context={"user_authenticated": user_authenticated,
                     "form": form,
                     "pk": pk}
        )

    def post(self, request, pk):
        form = AddNewLinkForm(request.POST)

        if form.is_valid():
            link = form.save(commit=False)
            link.playlist_id = pk
            link.save()
        return redirect("home_target_n", target="personal_playlists")
    


def LogOutView(request):
    logout(request)
    return redirect("home_n")
