from django.db import models
from datetime import datetime
from accounts.models import User
import uuid


# keeps all info about playlist of links 
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
    deleted = models.BooleanField(default=False, editable=False)
    background_color = models.CharField(
        max_length=8,
        editable=False,
        default="#F7F7F7"
    )
    inheritences_amount = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return "%s by %s" % (self.title, self.author)


# keeps links between private playlists and it's sharing link
class PrivateLink(models.Model):
    sharing_pk = models.UUIDField(primary_key=True, default=uuid.uuid4())
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        default="",
        editable=False,
        unique=True
    )


# keeps time when intented playlist gonna be deleted
# and is used into celery task for deleting
class DeletingTask(models.Model):
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, default="", editable=False
    )
    cherished_time = models.DateTimeField(
        default=datetime.now(),
        editable=False
    )

    def __str__(self):
        return "%s gonna be deleted at %s" % (
            self.playlist, self.cherished_time
        )


# all link's info
class Link(models.Model):
    link = models.URLField(max_length=128)
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, default="", editable=False
    )
    description = models.CharField(max_length=124, blank=True)
    check_relevance = models.BooleanField(default=False)

    def __str__(self):
        return "%s in %s" % (self.link, self.playlist)


# is used for celery task for checking if link is out of date
class LinkRelevance(models.Model):
    link = models.ForeignKey(
        Link, on_delete=models.CASCADE, default="", editable=False
    )
    status_code = models.IntegerField(max_length=3)

    def __str__(self):
        return "Check relevance for %s" % self.link


# keeping likes/diskikes.
# -1 dislike
# +1 like
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


# keeps info about which playlists are inherited by which user
class Inheritence(models.Model):
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, default="", editable=False
    )
    inherited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default="", editable=False
    )

    def __str__(self):
        return "%s inherited by %s" % (
            self.playlist.id, self.inherited_by.username
        )


# keeps all comments from all playlists
class Comment(models.Model):
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, default="", editable=False
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default="", editable=False
    )
    comment = models.CharField(max_length=124, blank=False)

    def __str__(self):
        return "Comment from %s into %s playlist" % (
            self.author.id, self.playlist.id
        )