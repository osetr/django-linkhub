from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("sign_up/", SignUpView.as_view(), name="sign_up_n"),
    path("sign_in/", SignInView.as_view(), name="sign_in_n"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password_n"),
    path("set_password/", SetPasswordView.as_view(), name="set_password_n"),
    path("reset_password/", ResetPasswordView.as_view(), name="reset_password_n"),



    path("signup/", signup, name="account_signup"),
    path("login/", login, name="account_login"),
    path("password/change/", password_change,
         name="account_change_password"),
    path("password/set/", password_set, name="account_set_password"),
    path("inactive/", account_inactive, name="account_inactive"),

    # E-mail
    path("email/", email, name="account_email"),
    path("confirm-email/", email_verification_sent,
         name="account_email_verification_sent"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", confirm_email,
            name="account_confirm_email"),

    # password reset
    path("password/reset/", password_reset,
         name="account_reset_password"),
    path("password/reset/done/", password_reset_done,
         name="account_reset_password_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
            ResetPasswordFromKeyView.as_view(),
            name="account_reset_password_from_key"),
    path("password/reset/key/done/", password_reset_from_key_done,
         name="account_reset_password_from_key_done"),
]
