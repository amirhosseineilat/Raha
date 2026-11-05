from django.db import models
from django.conf import settings
from django.db.models import Q, F


class AudioCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AudioContent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    sound = models.URLField()

    audio_category = models.ForeignKey(
        AudioCategory, on_delete=models.PROTECT, related_name="audio_contents"
    )

    def __str__(self):
        return self.name


class AudioSession(models.Model):
    class Status(models.TextChoices):
        PLAYING = "playing", "Playing"
        PAUSED = "paused", "Paused"
        COMPLETED = "completed", "Completed"
        STOPPED = "stopped", "Stopped"
        INTERRUPTED = "interrupted", "Interrupted"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="audio_sessions",
    )

    audio_content = models.ForeignKey(
        AudioContent, on_delete=models.PROTECT, related_name="audio_sessions"
    )

    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    last_position = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=100,
        choices=Status,
        default=Status.PLAYING,
    )

    class Meta:
        indexes = [
            models.Index(fields=["user", "started_at"], name="audio_user_started_idx")
        ]

        constraints = [
            models.CheckConstraint(
                condition=(Q(status__in=["playing", "paused"], ended_in__isnull=True))
                | Q(
                    status__in=["completed", "stopped", "interrupted"],
                    ended_at__isnull=False,
                )
                & Q(ended_at__gte=F("started_at")),
                name="audio_session_valid_status_and_time",
            ),
            models.CheckConstraint(
                condition=Q(last_position__gte=0), name="audio_last_position_gte_0"
            ),
        ]
