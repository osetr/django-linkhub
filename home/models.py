from django.db import models
from playlists.models import User

class IntroInfo(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default="", editable=False
    )
    show = models.BooleanField(default=True)

    def __str__(self):
        return "Show intro(%s) to %s" % (self.show, self.author.username)