from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Playlist, Link, Evaluating
from accounts.models import User
from .forms import AddNewPlaylistForm, AddNewLinkForm
from django.http import JsonResponse, HttpResponse
import re
from django.http import Http404, JsonResponse


def like_ajax(request, pk):
    playlist = Playlist.objects.get(pk=pk)
    try:
        evaluating = Evaluating.objects.filter(author=request.user, 
                                               playlist=playlist).get()
    except Evaluating.DoesNotExist:
        evaluating = Evaluating(state=1, 
                                author=request.user, 
                                playlist=playlist)
        playlist.likes += 1
        playlist.save()
        evaluating.save()
    else:
        # if playlist already liked
        if evaluating.state == 1:
            playlist.likes -= 1
            evaluating.state = 0
            evaluating.save()
            playlist.save()
        # if playlist still doesn't have evaluating
        elif evaluating.state == 0:
            playlist.likes += 1
            evaluating.state = 1
            evaluating.save()
            playlist.save()
        # if playlist was disliked
        elif evaluating.state == -1:
            playlist.likes += 1
            playlist.dislikes -= 1
            evaluating.state = 1
            evaluating.save()
            playlist.save()

    likes_amount = playlist.likes
    dislikes_amount = playlist.dislikes       
    if request.is_ajax():
        response = {'likes_amount': likes_amount, 
                    'dislikes_amount': dislikes_amount}

        return JsonResponse(response)
    else:
        raise Http404


def dislike_ajax(request, pk):
    playlist = Playlist.objects.get(pk=pk)
    evaluating = Evaluating.objects.filter(author=request.user, 
                                           playlist=playlist).get()
    if not evaluating:
        evaluating = Evaluating(state=-1,
                                author=request.user, 
                                playlist=playlist)
        playlist.dislikes += 1
        playlist.save()
        evaluating.save()
    else:
        # if playlist was liked
        if evaluating.state == 1:
            playlist.likes -= 1
            playlist.dislikes += 1
            evaluating.state = -1
            evaluating.save()
            playlist.save()
        # if playlist still doesn't have evaluating
        elif evaluating.state == 0:
            playlist.dislikes += 1
            evaluating.state = -1
            evaluating.save()
            playlist.save()
        # if playlist already disliked
        elif evaluating.state == -1:
            playlist.dislikes -= 1
            evaluating.state = 0
            evaluating.save()
            playlist.save()

    likes_amount = playlist.likes
    dislikes_amount = playlist.dislikes 
    if request.is_ajax():
        response = {'likes_amount': likes_amount, 'dislikes_amount': dislikes_amount}

        return JsonResponse(response)
    else:
        raise Http404


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


class ShowPlaylistView(View):
    def get(self, request, pk):
        user_authenticated = request.user.is_authenticated
        playlist = Playlist.objects.get(pk=pk)
        links = list(Link.objects.filter(playlist_id=playlist.id).values())
        author = User.objects.get(pk=playlist.author_id)

        return render(
            request,
            "show_playlist.html",
            context={"user_authenticated": user_authenticated,
                     "playlist": playlist,
                     "links": links,
                     "author": author,
                     "pk": pk}
        )
    


def LogOutView(request):
    logout(request)
    return redirect("home_n")

