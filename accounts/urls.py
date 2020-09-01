from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("sign_up/", SignUpView.as_view(), name="sign_up_n"),
    path("sign_in/", SignInView.as_view(), name="sign_in_n"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password_n"),
    path("set_password/", SetPasswordView.as_view(), name="set_password_n"),
    path("reset_password/", ResetPasswordView.as_view(), name="reset_password_n"),
    path(
        "confirm-email/",
        VerificationEmailSentView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "password_reset_done/",
        ResetPasswordDoneView.as_view(),
        name="reset_password_done_n",
    ),
    re_path(
        r"^password_reset_key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        ResetPasswordFromKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
    path(
        "password_reset_key_done/",
        ResetPasswordFromKeyDoneView.as_view(),
        name="reset_password_from_key_done_n",
    ),
]
