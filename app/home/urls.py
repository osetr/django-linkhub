from django.urls import path
from .views import HomeView


urlpatterns = [
    path(r"", HomeView.as_view(), name="home_n"),
]
