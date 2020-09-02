from django.db import models
from datetime import datetime
from accounts.models import User


class Playlist(models.Model):
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=260)
    date = models.DateTimeField(default=datetime.now(), editable=False)
    likes = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return "%s by %s" % (self.title, self.date)
