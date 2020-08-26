from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    rpassword = forms.CharField(required=False,
                                widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Enter unique name'})
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Enter email'})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Enter password'})
        self.fields['rpassword'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Repeat password'})

    class Meta:
        model = User
        fields = "__all__"

    
