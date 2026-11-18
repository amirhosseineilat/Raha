
from django import forms

from .models import UserNotificationSettings, NotificationPreference


class UserNotificationSettingsForm(forms.ModelForm):

    class Meta:
        model = UserNotificationSettings
        fields = ["is_enabled", "timezone"]


class NotificationPreferenceForm(forms.ModelForm):

    class Meta:
        model = NotificationPreference
        fields = ["is_enabled", "notification_time"]
        widgets = {
            "notification_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
        }
