from django.shortcuts import render
from .forms import (
    SignInForm,
    SignUpForm,
    ChangePasswordCustomForm,
    SetPasswordCustomForm,
)
from .models import User
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from allauth.account.views import LoginView, PasswordChangeView, PasswordSetView
from django.http import HttpResponseRedirect
from django.urls import reverse


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        user_authenticated = request.user.is_authenticated
        return render(
            request,
            "new_user.html",
            context={
                "form": form,
                "user_authenticated": user_authenticated,
                "active_page": "sign_up",
            },
        )

    def post(self, request):
        form = SignUpForm(request.POST)
        user_authenticated = request.user.is_authenticated
        if form.is_valid():
            form.save(request)
            return redirect("sign_in_n")
        return render(
            request,
            "new_user.html",
            context={
                "form": form,
                "user_authenticated": user_authenticated,
                "active_page": "sign_up",
            },
        )


class SignInView(LoginView):
    def get(self, request):
        form = SignInForm()
        return render(
            request,
            "login_user.html",
            context={"form": form, "active_page": "sign_in"},
        )

    def post(self, request):
        form = SignInForm(request.POST)
        errors = []
        username = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                errors.append("Your account has been deactivated")
            else:
                login(request, user)
                return redirect("home_n")
        else:
            errors.append("Incorrect username or password")
        return render(
            request,
            "login_user.html",
            context={"form": form, "errors": errors, "active_page": "sign_in"},
        )


class ChangePasswordView(PasswordChangeView):
    def get_success_url(self):
        return "/home"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = ChangePasswordCustomForm

    def render_to_response(self, context, **response_kwargs):
        user_authenticated = self.request.user.is_authenticated
        if not self.request.user.has_usable_password():
            return HttpResponseRedirect(reverse("set_password_n"))
        context.update(
            {"user_authenticated": user_authenticated, "active_page": "change_password"}
        )
        return super(PasswordChangeView, self).render_to_response(
            context, **response_kwargs
        )


class SetPasswordView(PasswordSetView):
    def get_success_url(self):
        return "/home"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = SetPasswordCustomForm

    def render_to_response(self, context, **response_kwargs):
        user_authenticated = self.request.user.is_authenticated
        context.update(
            {"user_authenticated": user_authenticated, "active_page": "change_password"}
        )
        return super(PasswordSetView, self).render_to_response(
            context, **response_kwargs
        )
