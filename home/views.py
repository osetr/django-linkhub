from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from playlists.models import Playlist, Link, Evaluating, Inheritence, DeletingTask, PrivateLink
from .models import IntroInfo
from accounts.models import User
from django.http import JsonResponse, HttpResponse
import re
from django.http import Http404, JsonResponse
from datetime import datetime, timedelta
import uuid


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
