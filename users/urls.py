from django.urls import path
from .views import *

urlpatterns = [
    path('new/', AddUser.as_view(), name='new_user')
]
