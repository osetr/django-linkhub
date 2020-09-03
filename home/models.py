from django.db import models
from datetime import datetime
from accounts.models import User


class Playlist(models.Model):
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=2500)
    date = models.DateTimeField(default=datetime.now(), editable=False)
    likes = models.IntegerField(default=0, editable=False)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return "%s by %s" % (self.title, self.date)
