from django.db import models
from datetime import datetime
from accounts.models import User


class Playlist(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default="", editable=False
    )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1024, blank=True)
    date = models.DateTimeField(default=datetime.now(), editable=False)
    likes = models.IntegerField(default=0, editable=False)
    dislikes = models.IntegerField(default=0, editable=False)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return "%s by %s" % (self.title, self.author)


class Link(models.Model):
    link = models.URLField(max_length=128)
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, default="", editable=False
    )
    description = models.CharField(max_length=124, blank=True)
    check_relevance = models.BooleanField(default=False)

    def __str__(self):
        return "%s in %s" % (self.link, self.playlist)


class Evaluating(models.Model):
    state = models.IntegerField(max_length=1, default=0)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default="", editable=False
    )
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, default="", editable=False
    )

    def __str__(self):
        return "%s of %s" % (self.author, self.playlist)


class Inheritence(models.Model):
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, default="", editable=False
    )
    inherited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default="", editable=False
    )

    def __str__(self):
        return "%s inherited by %s" % (self.playlist.id, self.inherited_by.username)


class IntroInfo(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default="", editable=False
    )
    show = models.BooleanField(default=True)

    def __str__(self):
        return "Show intro(%s) to %s" % (self.show, self.author.username)