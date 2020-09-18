from django.forms import ModelForm, CharField, HiddenInput
from .models import Playlist, Link


class AddNewPlaylistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter title"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter description"}
        )
        self.fields["is_private"].label = "Make private"

    class Meta:
        model = Playlist
        fields = "__all__"


class EditPlaylistForm(AddNewPlaylistForm):
    links = CharField(widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_private"].label = "Is private"
        self.fields["links"].label = ""


class AddNewLinkForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["link"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter link"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter short description"}
        )
        self.fields["check_relevance"].label = "Send message if link is out of date"

    class Meta:
        model = Link
        fields = "__all__"
