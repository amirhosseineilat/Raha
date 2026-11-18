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
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "ایمیل خود را وارد کنید",
            "autofocus": True,
        }),
    )


class OTPVerifyForm(forms.Form):
    otp = forms.CharField(
        label="کد تأیید",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "کد ۶ رقمی را وارد کنید",
            "inputmode": "numeric",
            "autocomplete": "one-time-code",
            "autofocus": True,
        }),
    )

    def clean_otp(self):
        otp = self.cleaned_data.get("otp")
        if not otp.isdigit():
            raise forms.ValidationError("کد باید فقط شامل عدد باشد.")
        return otp


class UserResetPassword(PasswordResetForm):
    pass


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "username": "نام کاربری",
            "email": "ایمیل",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "last_name": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "username": forms.TextInput(attrs={"autocomplete": "username"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
        }

    def clean_username(self):
        return self.cleaned_data.get("username") or None
