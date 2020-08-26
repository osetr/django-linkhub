from django.db import models
from datetime import datetime

class User(models.Model):
    login = models.CharField(max_length=20, 
                             verbose_name="user's login", 
                             unique=True)
    email = models.EmailField(verbose_name="users'email",
                              unique=True)
    password = models.CharField(max_length=120,
                                verbose_name="user's password")
    date_time = models.DateTimeField(default=datetime.now(), 
                                     editable=False)