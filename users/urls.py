from django.urls import path
from .views import *

urlpatterns = [
    path('new/', AddUser, name='add_user')
]
