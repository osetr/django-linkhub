from django import forms
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import (
    RegexValidator, EmailValidator,
    MaxLengthValidator, MinLengthValidator)


class UserForm(forms.ModelForm):
    pass_validator = RegexValidator(regex=r'[A-Za-z0-9@#$%^&+=]{8,}')

    password = forms.CharField(widget=forms.PasswordInput(), 
                               label='Password',
                               validators=[pass_validator])
    username = forms.CharField(label='Username',
                               validators=[
                                   RegexValidator(regex=r'[a-zA-Z0-9]+'),
                                   MaxLengthValidator(35),
                                   MinLengthValidator(5),  
                               ])
    email = forms.EmailField(label='Email',
                             validators=[EmailValidator])


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Enter unique name'})
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Enter email'})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Enter password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserAddForm(UserForm):
    rpassword = forms.CharField(widget=forms.PasswordInput(),
                                label='Repeat password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rpassword'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Repeat password'})

    def save(self, commit=True):
        new_user = super(UserAddForm, self).save(commit=False)
        new_user.password = make_password(new_user.password)
        if commit:
            new_user.save()
        return new_user


class UserLoginForm(UserForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Enter username'})
