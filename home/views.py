from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Playlist
from django.http import JsonResponse
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
        page_content = list(Playlist.objects.values())

        def amount_of_occurences(str):
            general_amount = 0
            for key in playlists_keys.split():
                general_amount += len(re.findall(key, str["title"]))
                general_amount += len(re.findall(key, str["description"]))
            return general_amount - (general_amount % 10)

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
            },
        )


def LogOutView(request):
    logout(request)
    return redirect("home_n")
