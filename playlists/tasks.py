from celery.task import periodic_task
from datetime import datetime, timedelta
from .models import DeletingTask, Playlist

@periodic_task(run_every=timedelta(seconds=1), name="delete_playlist")
def delete_playlist():
    try:
        task = DeletingTask.objects.first()
        if (task.cherished_time < datetime.now()):
            Playlist.objects.filter(pk=task.playlist.id).delete()
            print("Playlist {} was deleted".format(task.playlist.id))
        else:
            print("Waiting")
    except:
        print("There is no any tasks")
