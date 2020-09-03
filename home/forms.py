from django.forms import ModelForm
from .models import Playlist

class AddNewPlaylistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter title"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter description", "style": "resize: none;"}
        )
        self.fields["is_private"].label = "Make private"
    class Meta:
        model = Playlist
        fields = '__all__'