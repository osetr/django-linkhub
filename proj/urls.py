from django.contrib import admin
from django.urls import path, include
from users.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls")),
    path("", include("home.urls")),
]
