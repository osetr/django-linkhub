from django.urls import path
from .views import *

urlpatterns = [
    path("", Home.as_view(), name="main"),
    path("logout/", logout_view, name="logout"),
]
