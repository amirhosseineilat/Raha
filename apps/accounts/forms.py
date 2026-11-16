from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
)

from .models import User


class UserRegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "username")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        return username or None


class UserLoginForm(AuthenticationForm):

    username = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "ایمیل خود را وارد کنید",
                "autofocus": True,
            }
        ),
    )

class UserResetPassword(PasswordResetForm):
    pass