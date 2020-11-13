from django.urls import path
from .views import HomeView
from django.views.generic import RedirectView


urlpatterns = [
    path(r"", HomeView.as_view(), name="home_n"),
    path(r"favicon.ico", RedirectView.as_view(url='/full_static/images/favicon.ico'), name='favicon')
]
