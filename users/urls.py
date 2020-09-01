from django.urls import path
from .views import *

urlpatterns = [
    path("sign_up/", SignUpView.as_view(), name="sign_up_n"),
    path("sign_in/", SignInView.as_view(), name="sign_in_n"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password_n"),
    path("set_password/", SetPasswordView.as_view(), name="set_password_n"),
]
