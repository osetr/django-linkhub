from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from .models import (
    Playlist,
    Link,
    Evaluating,
    Inheritence,
    DeletingTask,
    LinkRelevance,
    PrivateLink,
    Comment
)
from home.models import IntroInfo
from accounts.models import User
from .forms import AddNewPlaylistForm, AddNewLinkForm
import re
from django.http import Http404, JsonResponse
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
import uuid
from project.settings import DELETING_PLAYLIST_TIME
from django.contrib.auth.mixins import LoginRequiredMixin
from .css_colors import CSS_COLORS, colors_amount


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
        if user_authenticated:
            playlists = list(
                Playlist.objects.filter(author=request.user.id).values()
            )

            if user_authenticated:
                inherited_playlists = list(
                    map(
                        lambda a: a["playlist_id"],
                        Inheritence
                        .objects
                        .filter(inherited_by=request.user)
                        .values(),
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
        else:
            return redirect("sign_in_n")

    def post(self, request):
        def filter_by_keys(playlists_keys, playlists):
            """
                Special function to exctract only required playlists
                from whole load. Take str with string of keys and playlists.
            """

            def amount_of_occurences(playlist):
                general_amount = 0
                for key in playlists_keys.split():
                    general_amount += len(
                        re.findall(key, playlist["title"])
                    )
                    general_amount += len(
                        re.findall(key, playlist["description"])
                    )
                return general_amount

            playlists.sort(
                key=lambda a: (amount_of_occurences(a), int(a["likes"])),
                reverse=True
            )
            playlists = list(filter(amount_of_occurences, playlists))
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
                        Inheritence
                        .objects
                        .filter(inherited_by=request.user)
                        .values(),
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


class AddNewLinkView(LoginRequiredMixin, View):
    """
        View for shortcut page for adding new links in playlist
    """
    login_url = "/sign_in/"

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
            if link.check_relevance:
                LinkRelevance.objects.create(
                    link=link,
                    status_code=0
                )
        return redirect("show_playlists_n")


class AddNewPlaylistView(LoginRequiredMixin, View):
    """
        View for adding new playlists
    """
    login_url = "/sign_in/"

    def get(self, request):
        user_authenticated = request.user.is_authenticated

        return render(
            request,
            "add_playlist.html",
            context={
                "user_authenticated": user_authenticated,  # adjust navbar functions
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


class EditPlaylistView(LoginRequiredMixin, View):
    """
        View for editing info about playlist(title, description)
        and adding new links, and managing old ones
    """
    login_url = "/sign_in/"

    def get(self, request, pk):
        # here we just extract all info about playlist
        # and put them into forms
        try:
            user_authenticated = request.user.is_authenticated

            playlist = Playlist.objects.get(pk=pk)

            playlist_deleted = playlist.deleted
            links = Link.objects.filter(playlist_id=pk).all()

            title = playlist.title
            description = playlist.description
            is_private = playlist.is_private
            form = AddNewPlaylistForm(
                {
                    "title": title,
                    "description": description,
                    "is_private": is_private
                }
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
        except Playlist.DoesNotExist:
            return redirect("show_playlists_n")

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

            links = list(
                map(
                    lambda a: re.search("link:(.*?),", a).group(1),
                    links
                )
            )
            descriptions = list(
                map(
                    lambda a: re.search("description:(.*?),", a).group(1),
                    descriptions
                )
            )
            checks = list(
                map(
                    lambda a: re.search("check:(.*?),", a).group(1), checks
                )
            )

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
                if db_link.link not in all_page_links:
                    db_link.delete()

            for page_link in page_links:
                try:
                    db_link = db_links.get(link=page_link["link"])
                    db_link.description = page_link["description"]
                    db_link.check_relevance = (
                        page_link["check_relevance"] == "true"
                    )
                    if db_link.check_relevance:
                        try:
                            LinkRelevance.objects.get(link=db_link)
                        except LinkRelevance.DoesNotExist:
                            LinkRelevance.objects.create(
                                link=db_link,
                                status_code=0
                            )
                    else:
                        try:
                            LinkRelevance.objects.get(link=db_link).delete()
                        except LinkRelevance.DoesNotExist:
                            print("Link still didn't require checking relevance!")
                    db_link.save()
                except Link.DoesNotExist:
                    ln = Link.objects.create(
                        link=page_link["link"],
                        description=page_link["description"],
                        check_relevance=page_link["check_relevance"] == "true",
                        playlist_id=pk,
                    )
                    if ln.check_relevance:
                        LinkRelevance.objects.create(
                            link=ln,
                            status_code=0
                        )

            playlist.save()
        return redirect("show_playlists_n")


class ShowPlaylistView(View):
    """
        View for showing all allowed info to user.
        If user is not owner of playlist, then he cann't
        take acces for buttons edit and add new link. 
    """
    def get(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except (Playlist.DoesNotExist, ValueError, ValidationError):
            try:
                playlist = PrivateLink.objects.get(sharing_pk=pk)
            except (PrivateLink.DoesNotExist, ValueError, ValidationError):
                return redirect("show_playlists_n")
            else:
                link = PrivateLink.objects.get(sharing_pk=pk)
                playlist = link.playlist
        else:
            playlist = Playlist.objects.get(pk=pk)
            if playlist.is_private and playlist.author != request.user:
                return redirect("show_playlists_n")

        user_authenticated = request.user.is_authenticated
        links = list(Link.objects.filter(playlist_id=playlist.id).values())
        author = User.objects.get(pk=playlist.author_id)

        # assemble all comments to current playlist
        comments = (
            Comment.objects.
            filter(playlist=playlist).
            order_by('id').
            reverse()
        )

        def process_date(date):
            return {
                date.day == datetime.now().day: date.time().strftime("%I:%M %P"),
                date.day == datetime.now().day - 1: 'yesterday ' + date.time().strftime("%I:%M %P"),
                date.day < datetime.now().day -1: date
            }[True]


        comments = {
            comment.id: 
            {
                "author": comment.author.username,
                "message": comment.comment,
                "date": process_date(comment.date),
                "color": CSS_COLORS[comment.author.id*3 % colors_amount],
            }
            for comment in comments
        }

        return render(
            request,
            "show_playlist.html",
            context={
                "user_authenticated": user_authenticated, # adjust navbar functions
                "playlist": playlist, # current playlist, which gonna be showed
                "links": links, # all links from current playlist
                "author": author, # keep author of playlist
                "pk": pk, # personal key of playlist for sharing functionality and editing
                "room_name": "room" + pk, # chat-room for current playlist
                "comments": comments, # comments dict for current playlist
            },
        )


def like_ajax(request, pk):
    playlist = Playlist.objects.get(pk=pk)
    if request.user.is_authenticated:
        try:
            evaluating = Evaluating.objects.filter(
                author=request.user, playlist=playlist
            ).get()
        except Evaluating.DoesNotExist:
            evaluating = Evaluating(
                state=1,
                author=request.user,
                playlist=playlist
            )
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
        response = {
            "likes_amount": likes_amount,
            "dislikes_amount": dislikes_amount
        }
        return JsonResponse(response)
    else:
        raise Http404


def dislike_ajax(request, pk):
    playlist = Playlist.objects.get(pk=pk)
    if request.user.is_authenticated:
        try:
            evaluating = Evaluating.objects.filter(
                author=request.user, playlist=playlist
            ).get()
        except Evaluating.DoesNotExist:
            evaluating = Evaluating(
                state=-1,
                author=request.user,
                playlist=playlist
            )
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
        response = {
            "likes_amount": likes_amount,
            "dislikes_amount": dislikes_amount
        }

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
            inheritence = Inheritence(
                playlist=playlist,
                inherited_by=current_user
            )
            inheritence.save()
            playlist.inheritences_amount += 1
            playlist.save()
            response = "inhereted successfuly"
    else:
        inheritence.delete()
        playlist.inheritences_amount -= 1
        playlist.save()
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
        DeletingTask.objects.create(
            playlist=playlist,
            cherished_time=datetime.now() + timedelta(
                seconds=DELETING_PLAYLIST_TIME
            )
        )
        playlist.save()
    except Playlist.DoesNotExist:
        response = {"response": "failed"}
    else:
        response = {"response": "success"}
    finally:
        return JsonResponse(response)


def restore_playlist_ajax(request, pk):
    try:
        playlist = Playlist.objects.get(pk=pk)
        playlist.deleted = False
        DeletingTask.objects.filter(playlist=playlist).delete()
        playlist.save()
    except Playlist.DoesNotExist:
        response = {"response": "failed"}
    else:
        response = {"response": "success"}
    finally:
        return JsonResponse(response)


def check_alive_ajax(request, pk):
    try:
        task = DeletingTask.objects.get(playlist_id=pk)
        time_future = task.cherished_time
        time_now = datetime.now()
        blur = (time_future-time_now).total_seconds()/DELETING_PLAYLIST_TIME
        if blur < 0:
            Playlist.objects.get(pk=pk).delete()
    except DeletingTask.DoesNotExist:
        response = {"response": "failed"}
    else:
        response = {"response": "success", "blur": blur}
    finally:
        return JsonResponse(response)


def create_private_link_ajax(request, pk):
    try:
        PrivateLink.objects.get(playlist_id=pk).delete()
    except PrivateLink.DoesNotExist:
        print("Link does not exist")
    finally:
        private_link = PrivateLink.objects.create(
            playlist_id=pk,
            sharing_pk=uuid.uuid4()
        )
    response = {"response": str(private_link.sharing_pk)}
    return JsonResponse(response)
