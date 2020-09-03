from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Playlist
from .forms import AddNewPlaylistForm, AddNewLinkForm
from django.http import JsonResponse, HttpResponse
import re


class HomeView(View):
    def get(self, request):
        user_authenticated = request.user.is_authenticated
        return render(
            request,
            "home.html",
            context={"user_authenticated": user_authenticated, 
                     "active_page": "home"},
        )

    def post(self, request):
        user_authenticated = request.user.is_authenticated
        playlists_keys = request.POST.get("playlists_keys", "")
        page_content = list(Playlist.objects.filter(is_private=0).values())
        request_of = request.POST.get('test', 'all')
        if not request_of:
            request_of = "owns"

        def amount_of_occurences(str):
            general_amount = 0
            for key in playlists_keys.split():
                general_amount += len(re.findall(key, str["title"]))
                general_amount += len(re.findall(key, str["description"]))
            return general_amount

        page_content.sort(
            key=lambda a: (amount_of_occurences(a), int(a["likes"])), 
            reverse=True
        )
        if not page_content:
            page_header = "Nothing found"
            page_content = "List is empty"
        else:
            page_header = "Playlist's list"
        return render(
            request,
            "home.html",
            context={
                "user_authenticated": user_authenticated,
                "active_page": "home",
                "page_header": page_header,
                "page_content": page_content,
                "user": request.user,
                "request_of": request_of,
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
        return redirect("add_new_playlist_n")


class AddNewLinkView(View):
    def get(self, request):
        form = AddNewLinkForm()
        user_authenticated = request.user.is_authenticated

        return render(
            request,
            "add_link.html",
            context={"user_authenticated": user_authenticated,
                     "form": form}
        )

    def post(self, request):
        form = AddNewLinkForm(request.POST)
        user_authenticated = request.user.is_authenticated

        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.author = request.user
            playlist.save()
        return redirect("add_new_link_n")
    


def LogOutView(request):
    logout(request)
    return redirect("home_n")
