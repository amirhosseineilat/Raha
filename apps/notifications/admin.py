from django.contrib import admin
from .models import UserNotificationSettings, NotificationPreference, NotificationLog


@admin.register(UserNotificationSettings)
class UserNotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "is_enabled", "timezone"]


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "notification_type",
        "is_enabled",
        "notification_time",
    ]


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "notification_type",
        "scheduled_for",
        "sent_at",
        "status",
        "error_message",
        "created_at",
    ]
