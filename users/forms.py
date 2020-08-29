from allauth.account.forms import (
    SignupForm, LoginForm, 
    ChangePasswordForm, SetPasswordForm)
from django import forms


class UserAddForm(SignupForm):
    def __init__(self, *args, **kwargs):
        self.field_order = [
                'username',
                'email',
                'password1',
                'password2'
            ]
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter unique name"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter email"}
        )
        self.fields['email'].label = "Email"
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repeat password"}
        )



class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your name"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter password"}
        )


class ChangePasswordCustomizedForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["oldpassword"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter current password"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repeat password"}
        )


class SetPasswordCustomizedForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repeat password"}
        )