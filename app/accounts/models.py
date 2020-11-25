from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class DeletingAccountProcess(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default="", editable=False
    )
    deleting_request_time = models.DateTimeField(default=datetime.now(), editable=False)

    def __str__(self):
        return "%s requested deleting account at %s" % (
            self.user, self.deleting_request_time
        )