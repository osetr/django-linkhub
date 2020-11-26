from datetime import datetime, timedelta
from .models import DeletingTask, Playlist, LinkRelevance
from accounts.models import DeletingAccountProcess
from django.core.mail import send_mail
from django.conf import settings
from celery.task import periodic_task
import requests


@periodic_task(run_every=timedelta(seconds=10), name="delete_account")
def delete_account():
    try:
        task = DeletingAccountProcess.objects.first()
        if (datetime.now() - task.deleting_request_time).total_seconds() > 86400:
            task.user.delete()
            print("Account deleted")
        else:
            pass
    except AttributeError:
        print("Account remover - blank shot")


@periodic_task(run_every=timedelta(seconds=5), name="delete_playlist")
def delete_playlist():
    try:
        task = DeletingTask.objects.first()
        if (task.cherished_time < datetime.now()):
            Playlist.objects.filter(pk=task.playlist.id).delete()
            print("Playlist {} was deleted".format(task.playlist.id))
        else:
            print("Waiting")
    except AttributeError:
        print("Playlists remover - blank shot")


@periodic_task(run_every=timedelta(seconds=15), name="check_relevance")
def check_relevnce():
    try:
        task = LinkRelevance.objects.first()
        link = task.link
        playlist = link.playlist
        author = playlist.author

        try:
            request_status = requests.get(task.link.link).status_code
        except:
            send_message = True
            message = (
                'Check pls link ' +
                link.link +
                ' from playlist "' +
                playlist.title +
                '". There are some issues with it!'
            )
        else:
            if not task.status_code:
                task.status_code = request_status
                print("Status code was created!")
                send_message = False
            elif task.status_code != request_status:
                message = (
                    'Check pls link ' +
                    link.link +
                    ' from playlist "' +
                    playlist.title +
                    '". Something happaned with status code!'
                )
                send_message = True
            else:
                send_message = False
        finally:
            if send_message:
                subject = 'Something went wrong'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [author.email]
                send_mail(subject, message, email_from, recipient_list)
                print("Message sended")
                link.check_relevance = 0
                link.save()
                task.delete()
            else:
                task.delete()
                task.save()
    except AttributeError:
        print("Checking relevance - blank shot")
