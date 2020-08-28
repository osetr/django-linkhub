from django.shortcuts import render
from .forms import UserAddForm, UserLoginForm
from .models import User
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from allauth.account.views import LoginView


class AddUser(View):
    def get(self, request):
        form = UserAddForm()
        return render(request, "new_user.html", context={"form": form})

    def post(self, request):
        form = UserAddForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect("login_user")
        return render(request, "new_user.html", context={"form": form})


class LoginUser(LoginView):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "login_user.html", context={"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        errors = []
        username = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                errors.append("Your account has been deactivated")
            else:
                login(request, user)
                return redirect("main")
        else:
            errors.append("Incorrect username or password")
        return render(
            request, "login_user.html", context={"form": form, 
                                                 "errors": errors}
        )
