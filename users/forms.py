from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from events.forms import TailwindMixin


class RegisterForm(TailwindMixin, UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Password"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in [
            "username",
            "password1",
            "password2",
        ]:
            self.fields[fieldname].help_text = None


class LoginForm(TailwindMixin, AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["password"].widget.attrs.update({"placeholder": "Password"})
