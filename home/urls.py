from django.urls import path
from .views import *

urlpatterns = [
    path("home/", HomeView.as_view(), name="home_n"),
    path("logout/", LogOutView, name="logout_n"),
]
