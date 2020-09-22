from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Playlist, Link, Evaluating, Inheritence, IntroInfo
from accounts.models import User
from .forms import AddNewPlaylistForm, AddNewLinkForm
from django.http import JsonResponse, HttpResponse
import re
from django.http import Http404, JsonResponse


def like_ajax(request, pk):
    playlist = Playlist.objects.get(pk=pk)
    try:
        evaluating = Evaluating.objects.filter(
            author=request.user, playlist=playlist
        ).get()
    except Evaluating.DoesNotExist:
        evaluating = Evaluating(state=1, author=request.user, playlist=playlist)
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
        response = {"likes_amount": likes_amount, "dislikes_amount": dislikes_amount}

        return JsonResponse(response)
    else:
        raise Http404


def dislike_ajax(request, pk):
    playlist = Playlist.objects.get(pk=pk)
    try:
        evaluating = Evaluating.objects.filter(
            author=request.user, playlist=playlist
        ).get()
    except Evaluating.DoesNotExist:
        evaluating = Evaluating(state=-1, author=request.user, playlist=playlist)
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
        response = {"likes_amount": likes_amount, "dislikes_amount": dislikes_amount}

        return JsonResponse(response)
    else:
        raise Http404


def inherite_ajax(request, pk):
    playlist = Playlist.objects.get(pk=pk)
    current_user = request.user
    try:
        inheritence = Inheritence.objects.filter(
            inherited_by=current_user, playlist=playlist
        ).get()
    except Inheritence.DoesNotExist:
        if not playlist.is_private:
            inheritence = Inheritence(playlist=playlist, inherited_by=current_user)
            inheritence.save()
            response = "inhereted successfuly"
    else:
        inheritence.delete()
        response = "inheretence deleted"
    if request.is_ajax():
        response = {"response": response}

        return JsonResponse(response)
    else:
        raise Http404


def show_introduction_ajax(request):
    introinfo = IntroInfo.objects.filter(author=request.user).get()

    if introinfo.show == 0:
        introinfo.show = 1
    else:
        introinfo.show = 0
    introinfo.save()

    if request.is_ajax():
        response = {"response": "success"}

        return JsonResponse(response)
    else:
        raise Http404


def remove_playlist_ajax(request, pk):
    try:
        playlist = Playlist.objects.get(pk=pk)
        playlist.deleted = True
        playlist.save()
    except:
        response = {"response": "failed"}
    else:
        response = {"response": "success"}
    finally:
        return JsonResponse({"response": "success"})


def restore_playlist_ajax(request, pk):
    try:
        playlist = Playlist.objects.get(pk=pk)
        playlist.deleted = False
        playlist.save()
    except:
        response = {"response": "failed"}
    else:
        response = {"response": "success"}
    finally:
        return JsonResponse({"response": "success"})


class HomeView(View):
    """
        View to show introductory info and availability
        of site functionality, depending on either user 
        is authenticated or not.
    """

    def get(self, request):
        user_authenticated = request.user.is_authenticated
        inherited_playlists = []
        show = True

        if user_authenticated:
            try:
                introinfo = IntroInfo.objects.filter(author=request.user).get()
                show = introinfo.show
            except IntroInfo.DoesNotExist:
                introinfo = IntroInfo(author=request.user)
                introinfo.save()
            inherited_playlists = list(
                map(
                    lambda a: a["playlist_id"],
                    Inheritence.objects.filter(inherited_by=request.user).values(),
                )
            )
        return render(
            request,
            "home.html",
            context={
                "user_authenticated": user_authenticated,  # availability of site functionality
                "active_page": "home",  # separeate active and non active pages on navbar
                "show": show,  # show ot not introductory info
            },
        )


class ShowPlaylistsView(View):
    """
    This class based view created to show playlists list, 
    depending on user's request. It gonna work either user 
    require their own playlists(plus inherited) or searching
    by keys. Actually GET request serves for first one and
    POST for second one.
    """

    def get(self, request):
        user_authenticated = request.user.is_authenticated
        playlists = list(Playlist.objects.filter(author=request.user.id).values())

        if user_authenticated:
            inherited_playlists = list(
                map(
                    lambda a: a["playlist_id"],
                    Inheritence.objects.filter(inherited_by=request.user).values(),
                )
            )
        else:
            inherited_playlists = []

        for playlist_pk in inherited_playlists:
            playlists.append(Playlist.objects.get(pk=playlist_pk))
        # at this point we have all playlists(own and inherited)
        # in on variable "playlists"

        # set html page header and content depending on playlists presence
        if not playlists:
            page_header = "Nothing found"
            list_empty = True
        else:
            page_header = "Playlist's list"
            list_empty = False
        return render(
            request,
            "show_playlists.html",
            context={
                "user_authenticated": user_authenticated,  # set availability of inheritence
                "page_header": page_header,  # html page header
                "playlists": playlists,  # all playlists (own&inherited)
                "active_page": "my_playlists",  # separeate active and non active pages on navbar
                "list_empty": list_empty,  # boolean, required for either showing content or not
                "inherited_playlists": inherited_playlists,  # check if playlist is allready inherited
            },
        )

    def post(self, request):
        def filter_by_keys(str, playlists):
            """
                Special function to exctract only required playlists
                from whole load. Take str with string of keys and playlists.
            """

            def amount_of_occurences(str):
                general_amount = 0
                for key in playlists_keys.split():
                    general_amount += len(re.findall(key, str["title"]))
                    general_amount += len(re.findall(key, str["description"]))
                return general_amount

            playlists.sort(
                key=lambda a: (amount_of_occurences(a), int(a["likes"])), reverse=True
            )
            return playlists

        user_authenticated = request.user.is_authenticated
        playlists_keys = request.POST.get("playlists_keys", "")
        playlists = list(Playlist.objects.values())
        inherited_playlists = []

        if not playlists:
            page_header = "Nothing found"
            playlists = "List is empty"
            list_empty = True
        else:
            if user_authenticated:
                inherited_playlists = list(
                    map(
                        lambda a: a["playlist_id"],
                        Inheritence.objects.filter(inherited_by=request.user).values(),
                    )
                )
            playlists = filter_by_keys(playlists_keys, playlists)  # searching by keys
            page_header = "Playlist's list"
            list_empty = False
        return render(
            request,
            "show_playlists.html",
            context={
                "user_authenticated": user_authenticated,  # set availability of inheritence
                "page_header": page_header,  # html page header
                "playlists": playlists,  # all playlists (own&inherited)
                "list_empty": list_empty,  # boolean, required for either showing content or not
                "inherited_playlists": inherited_playlists,  # check if playlist is allready inherited
            },
        )


class AddNewLinkView(View):
    """
        View for shortcut page for adding new links in playlistw
    """

    def get(self, request, pk):
        form = AddNewLinkForm()
        user_authenticated = request.user.is_authenticated

        return render(
            request,
            "add_link.html",
            context={
                "user_authenticated": user_authenticated,  # adjust navbar functions
                "form": form,
                "pk": pk,  # pk of current playlist for save button request
            },
        )

    def post(self, request, pk):
        form = AddNewLinkForm(request.POST)

        if form.is_valid():
            link = form.save(commit=False)
            link.playlist_id = pk
            link.save()
        return redirect("show_playlists_n")


class AddNewPlaylistView(View):
    """
        View for adding new playlists
    """

    def get(self, request):
        form = AddNewPlaylistForm()
        user_authenticated = request.user.is_authenticated

        return render(
            request,
            "add_playlist.html",
            context={
                "user_authenticated": user_authenticated,  # adjust navbar functions
                "form": form,
            },
        )

    def post(self, request):
        form = AddNewPlaylistForm(request.POST)

        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.background_color = request.POST.get("color", "")
            playlist.author = request.user
            playlist.save()
        return redirect("show_playlists_n")


class EditPlaylistView(View):
    """
        View for editing info about playlist(title, description)
        and adding new links, and managing old ones
    """

    def get(self, request, pk):
        # here we just extract all info about playlist
        # and put them into forms
        user_authenticated = request.user.is_authenticated

        playlist = Playlist.objects.get(pk=pk)

        playlist_deleted = playlist.deleted
        links = Link.objects.filter(playlist_id=pk).all()

        title = playlist.title
        description = playlist.description
        is_private = playlist.is_private
        form = AddNewPlaylistForm(
            {"title": title, "description": description, "is_private": is_private}
        )

        return render(
            request,
            "edit_playlist.html",
            context={
                "form": form,  # form with all required data in it
                "pk": pk,  # pk of current playlist for ajax requests
                "user_authenticated": user_authenticated,  # adjust navbar functions
                "links": links,  # old links of current playlist
                "playlist_deleted": playlist_deleted,  # boolean to determine if playlist is deleted
            },
        )

    def post(self, request, pk):
        def data_to_json(data):
            """
                Extract data from all links and put it
                into convinient view(list of dictionries)
                Actually this def takes only data parametr,
                that have to get data from hidden field 
                on front-end. Front-end save it in format:
                " link:www.link.com, description:some description, check_relevance: true(false), "
            """
            links = re.findall("link:.*?,", data)
            descriptions = re.findall("description:.*?,", data)
            checks = re.findall("check:.*?,", data)

            links = list(map(lambda a: re.search("link:(.*?),", a).group(1), links))
            descriptions = list(
                map(lambda a: re.search("description:(.*?),", a).group(1), descriptions)
            )
            checks = list(map(lambda a: re.search("check:(.*?),", a).group(1), checks))

            result = [
                {
                    "link": links[i],
                    "description": descriptions[i],
                    "check_relevance": checks[i],
                }
                for i in range(len(links))
            ]

            return result

        form = AddNewPlaylistForm(request.POST)

        # in following code:
        # page_links - links from frontend(existing and new)
        # db_links - already existing links from database
        if form.is_valid():
            playlist = Playlist.objects.get(pk=pk)
            playlist.title = form.cleaned_data["title"]
            playlist.description = form.cleaned_data["description"]
            playlist.is_private = form.cleaned_data["is_private"]

            page_links = data_to_json(request.POST["links"])

            db_links = Link.objects.filter(playlist_id=pk).all()

            all_page_links = [page_link["link"] for page_link in page_links]
            for db_link in db_links:
                if not db_link.link in all_page_links:
                    db_link.delete()

            for page_link in page_links:
                try:
                    db_link = db_links.get(link=page_link["link"])
                    db_link.description = page_link["description"]
                    db_link.check_relevance = page_link["check_relevance"] == "true"
                    db_link.save()
                except:
                    Link.objects.create(
                        link=page_link["link"],
                        description=page_link["description"],
                        check_relevance=page_link["check_relevance"] == "true",
                        playlist_id=pk,
                    )

            playlist.save()
        return redirect("show_playlists_n")


class ShowPlaylistView(View):
    def get(self, request, pk):
        user_authenticated = request.user.is_authenticated
        playlist = Playlist.objects.get(pk=pk)
        links = list(Link.objects.filter(playlist_id=playlist.id).values())
        author = User.objects.get(pk=playlist.author_id)

        return render(
            request,
            "show_playlist.html",
            context={
                "user_authenticated": user_authenticated,
                "playlist": playlist,
                "links": links,
                "author": author,
                "pk": pk,
            },
        )


def LogOutView(request):
    logout(request)
    return redirect("home_n")
