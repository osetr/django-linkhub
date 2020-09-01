from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect


class HomeView(View):
    def get(self, request):
        user_authenticated = request.user.is_authenticated
        return render(
            request,
            "home.html",
            context={"user_authenticated": user_authenticated, "active_page": "home"},
        )


def LogOutView(request):
    logout(request)
    return redirect("home_n")
