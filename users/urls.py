from django.urls import path
from .views import *

urlpatterns = [
    path("new/", AddUser.as_view(), name="new_user"),
    path("login/", LoginUser.as_view(), name="login_user"),
]
