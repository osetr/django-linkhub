from django.db import models
from datetime import datetime
from accounts.models import User


class Playlist(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default="", editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=2500)
    date = models.DateTimeField(default=datetime.now(), editable=False)
    likes = models.IntegerField(default=0, editable=False)
    dislikes = models.IntegerField(default=0, editable=False)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return "%s by %s" % (self.title, self.author)


class Link(models.Model):
    link = models.URLField(max_length=128)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, default="", editable=False)
    description = models.CharField(max_length=124)
    check_relevance = models.BooleanField(default=False)

    def __str__(self):
        return "%s in %s" % (self.link, self.playlist)