from django.db import models
from django.conf import settings
from .validators import validate_timezone


class UserNotificationSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_notification_settings",
    )

    is_enabled = models.BooleanField(default=True)
    timezone = models.CharField(
        max_length=64, default="UTC", validators=[validate_timezone]
    )


class NotificationPreference(models.Model):
    class NotificationType(models.TextChoices):
        MOOD_REMINDER = "mood_reminder", "Mood Reminder"
        BREATHING_REMINDER = "breathing_reminder", "Breathing Reminder"
        RELAXATION_REMINDER = "relaxation_reminder", "Relaxation Reminder"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preference",
    )

    notification_type = models.CharField(
        max_length=50, choices=NotificationType.choices
    )
    is_enabled = models.BooleanField(default=True)
    notification_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "notification_type"],
                name="unique_user_notification_type",
            )
        ]


class NotificationLog(models.Model):
    class NotificationType(models.TextChoices):
        MOOD_REMINDER = "mood_reminder", "Mood Reminder"
        BREATHING_REMINDER = "breathing_reminder", "Breathing Reminder"
        RELAXATION_REMINDER = "relaxation_reminder", "Relaxation Reminder"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_log",
    )

    notification_type = models.CharField(
        max_length=50, choices=NotificationType.choices
    )
    scheduled_for = models.DateTimeField()
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.PENDING
    )

    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["user", "scheduled_for"], name="user_scheduled_for_idx"
            )
        ]
