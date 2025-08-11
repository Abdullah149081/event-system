from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from events.forms import TailwindMixin


class RegisterForm(UserCreationForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-blue-300"
                }
            )

        # Remove help text for specific fields
        for fieldname in [
            "username",
            "password1",
            "password2",
        ]:
            self.fields[fieldname].help_text = None


class LoginForm(TailwindMixin, AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
