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

    def post(self, request):
        user_authenticated = request.user.is_authenticated
        name = request.POST.get("name", "")
        return render(
            request,
            "home.html",
            context={"user_authenticated": user_authenticated, "active_page": "home", "name": name},
        )


def LogOutView(request):
    logout(request)
    return redirect("home_n")
