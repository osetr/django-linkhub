from django.shortcuts import render
from .forms import UserAddForm, UserLoginForm, ChangePasswordCustomizedForm, SetPasswordCustomizedForm
from .models import User
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from allauth.account.views import LoginView, PasswordChangeView, PasswordSetView
from django.http import HttpResponseRedirect
from django.urls import reverse

class AddUser(View):
    def get(self, request):
        form = UserAddForm()
        user_authenticated = request.user.is_authenticated
        return render(request, "new_user.html", context={"form": form,
                                                         "user_authenticated": user_authenticated,
                                                         "active_page": "new_user"})

    def post(self, request):
        form = UserAddForm(request.POST)
        user_authenticated = request.user.is_authenticated
        if form.is_valid():
            form.save(request)
            return redirect("login_user")
        return render(request, "new_user.html", context={"form": form,
                                                         "user_authenticated": user_authenticated,
                                                         "active_page": "new_user"})


class LoginUser(LoginView):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "login_user.html", context={"form": form,
                                                           "active_page": "login_user"})

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
                                                 "errors": errors,
                                                 "active_page": "login_user"}
        )


class ChangePassword(PasswordChangeView):
    def get_success_url(self):
        return '/home'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = ChangePasswordCustomizedForm

    def render_to_response(self, context, **response_kwargs):
        user_authenticated = self.request.user.is_authenticated
        if not self.request.user.has_usable_password():
            return HttpResponseRedirect(reverse('set_pass'))
        context.update({"user_authenticated": user_authenticated, "active_page": "change_password"})
        return super(PasswordChangeView, self).render_to_response(
            context, **response_kwargs)


class SetPassword(PasswordSetView):
    def get_success_url(self):
        return '/home'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = SetPasswordCustomizedForm


    def render_to_response(self, context, **response_kwargs):
        user_authenticated = self.request.user.is_authenticated
        context.update({"user_authenticated": user_authenticated, "active_page": "change_password"})
        return super(PasswordSetView, self).render_to_response(
            context, **response_kwargs)

