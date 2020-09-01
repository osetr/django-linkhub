from django.shortcuts import render
from .forms import (
    SignInForm,
    SignUpForm,
    ChangePasswordCustomForm,
    SetPasswordCustomForm,
    ResetPasswordCustomForm,
    ResetPasswordKeyCustomForm,
)
from .models import User
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from allauth.account.views import *
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy


class SignUpView(SignupView):
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        user_authenticated = self.request.user.is_authenticated
        ret.update({"user_authenticated": user_authenticated, "active_page": "sign_up"})
        return ret


class SignInView(LoginView):
    form_class = SignInForm

    def get_context_data(self, **kwargs):
        errors = []
        if self.request.method == "POST":
            username = self.request.POST["login"]
            password = self.request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    errors.append("Your account has been deactivated")
                else:
                    login(request, user)
                    return redirect("home_n")
            else:
                errors.append("Incorrect username or password")
        ret = super().get_context_data(**kwargs)
        user_authenticated = self.request.user.is_authenticated
        ret.update(
            {
                "user_authenticated": user_authenticated,
                "active_page": "sign_in",
                "errors": errors,
            }
        )
        return ret


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


class ResetPasswordView(PasswordResetView):
    form_class = ResetPasswordCustomForm
    success_url = reverse_lazy("reset_password_done_n")

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        user_authenticated = self.request.user.is_authenticated
        ret.update(
            {"user_authenticated": user_authenticated, "active_page": "reset_password"}
        )
        return ret


class ResetPasswordDoneView(PasswordResetDoneView):
    pass


class ResetPasswordFromKeyView(PasswordResetFromKeyView):
    form_class = ResetPasswordKeyCustomForm
    success_url = reverse_lazy("reset_password_from_key_done_n")
    

class ResetPasswordFromKeyDoneView(PasswordResetFromKeyDoneView):
    pass


class VerificationEmailSentView(EmailVerificationSentView):
    pass


class ConfirmEmailView(ConfirmEmailView):
    pass
    