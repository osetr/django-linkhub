from celery.task import periodic_task
from datetime import datetime, timedelta
from .models import DeletingTask, Playlist, LinkRelevance
from django.core.mail import send_mail
from django.conf import settings
import requests


@periodic_task(run_every=timedelta(seconds=10), name="delete_playlist")
def delete_playlist():
    try:
        task = DeletingTask.objects.first()
        if (task.cherished_time < datetime.now()):
            Playlist.objects.filter(pk=task.playlist.id).delete()
            print("Playlist {} was deleted".format(task.playlist.id))
        else:
            print("Waiting")
    except:
        print("There is no any work for playlists remover")


@periodic_task(run_every=timedelta(seconds=10), name="check_relevance")
def check_relevnce():
    try:
        task = LinkRelevance.objects.first()
        request_status = requests.get(task.link.link).status_code
        link = task.link
        playlist = link.playlist
        author = playlist.author
        if task.status_code != request_status:
            subject = 'Something went wrong'
            message = 'Check pls link ' + link.link + ' from playlist "' + playlist.title + '". Something happaned with status code!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [author.email]
            send_mail( subject, message, email_from, recipient_list)
            print("message sended")
            task.delete()
        else:
            task.delete()
            LinkRelevance.objects.create(
                status_code=request_status, 
                link=link
            )
    except:
        print("There is no any work for checking relevance")
