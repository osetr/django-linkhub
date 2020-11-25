from django.contrib.auth import login, authenticate, logout
from .forms import (
    SignInForm,
    SignUpForm,
    ChangePasswordCustomForm,
    SetPasswordCustomForm,
    ResetPasswordCustomForm,
    ResetPasswordKeyCustomForm,
)
from django.views.generic import View
from django.shortcuts import redirect
from allauth.account.views import (
    SignupView,
    LoginView,
    PasswordChangeView,
    PasswordSetView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,
    EmailVerificationSentView,
    ConfirmEmailView
)
from .models import DeletingAccountProcess
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.utils import IntegrityError
from django.http import Http404, JsonResponse
# all views here are just overrided allauth module views.
# this approach helps to use benifits of allauth views.
# overriding is necessary to assign proper forms into views,
# put corresponding contexts and reassign success url,
# depending on case.


class SignUpView(SignupView):
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        user_authenticated = self.request.user.is_authenticated
        new_context = {
            "user_authenticated": user_authenticated,
            "active_page": "sign_up"
        }
        ret.update(new_context)
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
                    login(kwargs['request'], user)
                    return redirect("home_n")
            else:
                errors.append("Incorrect username or password")
        ret = super().get_context_data(**kwargs)
        user_authenticated = self.request.user.is_authenticated
        new_context = {
            "user_authenticated": user_authenticated,
            "active_page": "sign_in",
            "errors": errors,
        }
        ret.update(new_context)
        return ret


class ChangeUsername(View):
    def post(self, request):
        user = request.user
        user.username = request.POST['username']
        try:
            user.save()
            return redirect("settings_n")
        except:
            return redirect(
                reverse(
                    "settings_n",
                    kwargs={'error': 'Username already in use'}
                )
            )


class ChangePasswordView(PasswordChangeView):
    template_name = "account/settings.html"
    def get_success_url(self):
        return "/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = ChangePasswordCustomForm

    def render_to_response(self, context, **response_kwargs):
        username_change_error = self.request.resolver_match.kwargs.get('error', '')
        user_authenticated = self.request.user.is_authenticated
        if not self.request.user.has_usable_password():
            return HttpResponseRedirect(reverse("set_password_n"))

        try:
            DeletingAccountProcess.objects.get(user=self.request.user)
            account_process_deleting = True
        except DeletingAccountProcess.DoesNotExist:
            account_process_deleting = False        

        new_context = {
            "user_authenticated": user_authenticated,
            "active_page": "settings",
            "username": self.request.user.username,
            "username_error": username_change_error,
            "account_process_deleting": account_process_deleting,
        }
        context.update(new_context)
        return super(PasswordChangeView, self).render_to_response(
            context, **response_kwargs
        )


class SetPasswordView(PasswordSetView):
    def get_success_url(self):
        return "/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = SetPasswordCustomForm

    def render_to_response(self, context, **response_kwargs):
        user_authenticated = self.request.user.is_authenticated
        new_context = {
            "user_authenticated": user_authenticated,
            "active_page": "settings"
        }
        context.update(new_context)
        return super(PasswordSetView, self).render_to_response(
            context, **response_kwargs
        )


class ResetPasswordView(PasswordResetView):
    form_class = ResetPasswordCustomForm
    success_url = reverse_lazy("reset_password_done_n")

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        user_authenticated = self.request.user.is_authenticated
        new_context = {
            "user_authenticated": user_authenticated,
            "active_page": "reset_password"
        }
        ret.update(new_context)
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


def LogOutView(request):
    logout(request)
    return redirect("home_n")


def delete_account_ajax(request):
    try:
        DeletingAccountProcess.objects.get(user=request.user).delete()
        action = "Deleting process suspended"
    except DeletingAccountProcess.DoesNotExist:
        DeletingAccountProcess.objects.create(user=request.user)
        action = "Deleting process started"
    if request.is_ajax():
        response = {"response": "success", "action": action}
        return JsonResponse(response)
    else:
        raise Http404