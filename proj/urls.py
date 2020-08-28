from django.contrib import admin
from django.urls import path, include
from users.views import *

urlpatterns = [
    path("admin/", admin.site.urls), 
    path('accounts/', include('allauth.urls')),
    path("users/", include("users.urls")),
    path("home/", include("home.urls")),
]
