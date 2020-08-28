from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect


class Home(View):
    def get(self, request):
        return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("main")