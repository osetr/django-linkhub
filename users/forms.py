from django import forms
from .models import User
from django.contrib.auth.hashers import make_password, check_password


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), 
                               label='Password')
    rpassword = forms.CharField(widget=forms.PasswordInput(),
                                label='Repeat password')
    login = forms.CharField(label='Login')
    email = forms.EmailField(label='Email')


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

    def save(self, commit=True):
        new_user = super(UserForm, self).save(commit=False)
        new_user.password = make_password(new_user.password)
        if commit:
            new_user.save()
        return new_user