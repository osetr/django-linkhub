from django.forms import ModelForm
from .models import Playlist, Link


class AddNewPlaylistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter1 title"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter description"}
        )
        self.fields["is_private"].label = "Make private"

    class Meta:
        model = Playlist
        fields = "__all__"


class AddNewLinkForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["link"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter link", "autocomplete": "off"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter short description", "autocomplete": "off"}
        )
        self.fields["check_relevance"].label = "Notify me if link is out of date"

    class Meta:
        model = Link
        fields = "__all__"
