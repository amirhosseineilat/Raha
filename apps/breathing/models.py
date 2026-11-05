from django.db import models
from django.db.models import Q
from django.conf import settings


class BreathingExercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    inhale_time = models.PositiveIntegerField()
    holding = models.PositiveIntegerField()
    exhale = models.PositiveIntegerField()

    guidance_audio = models.URLField(blank=True)
    animation_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(inhale_time__gte=0), name="Breathing_inhale_time_gte_0"
            ),
            models.CheckConstraint(
                condition=Q(holding__gte=0), name="Breathing_holding_gte_0"
            ),
            models.CheckConstraint(
                condition=Q(exhale__gte=0), name="Breathing_exhale_gte_0"
            ),
        ]


class BreathingSession(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"
        INTERRUPTED = "interrupted", "Interrupted"

    class Feedback(models.TextChoices):
        IMPROVED = "improved", "Improved"
        UNCHANGED = "unchanged", "Unchanged"
        WORSENED = "worsened", "Worsened"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="breathing_sessions",
    )

    breathing_exercise = models.ForeignKey(
        BreathingExercise, on_delete=models.PROTECT, related_name="breathing_sessions"
    )

    duration = models.PositiveIntegerField()
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=100, choices=Status, default=Status.IN_PROGRESS
    )
    feedback = models.CharField(
        max_length=100,
        choices=Feedback.choices,
        null=True,
        blank=True,
    )

    feedback_note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.breathing_exercise.name}"

    class Meta:
        indexes = [
            models.Index(
                fields=["user", "started_at"],
                name="breath_user_started_idx",
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(duration__gt=0),
                name="breath_session_duration_gt_0",
            ),
            models.CheckConstraint(
                condition=(
                    Q(status="in_progress", ended_at__isnull=True)
                    | (
                        Q(
                            status__in=[
                                "completed",
                                "abandoned",
                                "interrupted",
                            ]
                        )
                        & Q(ended_at__isnull=False)
                        & Q(ended_at__gte=F("started_at"))
                    )
                ),
                name="breath_session_valid_status_and_time",
            ),
            models.CheckConstraint(
                condition=(
                    Q(feedback__isnull=True)
                    | Q(
                        status="completed",
                        feedback__in=[
                            "improved",
                            "unchanged",
                            "worsened",
                        ],
                    )
                ),
                name="breath_session_feedback_only_after_completion",
            ),
        ] 
