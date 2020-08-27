from django.shortcuts import render
from .forms import UserAddForm, UserLoginForm
from .models import User
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate


class AddUser(View):
    
    def get(self, request):
        form = UserAddForm()
        return render(request, "new_user.html", context={"form": form})

    def post(self, request):
        form = UserAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_user")
        return render(request, "new_user.html", context={"form": form})


class LoginUser(View):
    
    def get(self, request):
        form = UserLoginForm()
        return render(request, "login_user.html", context={"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        return render(request, "login_user.html", context={"form": form})