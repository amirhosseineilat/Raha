from django.db import models
from django.db.models import Q
from django.conf import settings


class BreathingExercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    inhale_time = models.PositiveIntegerField()
    holding = models.PositiveIntegerField()
    exhale = models.PositiveIntegerField()

    guidance_audio = models.CharField(max_length=255)
    animation_url = models.CharField(max_length=255)

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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="breathing_session",
    )

    breathing_exercise = models.ForeignKey(
        BreathingExercise, on_delete=models.PROTECT, related_name="breathing_session"
    )

    duration = models.PositiveIntegerField()
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()

    status = models.CharField(max_length=100)
    feedback = models.CharField(max_length=100)

    feedback_note = models.TextField()

    def __str__(self):
        return f"{self.user.email} - {self.breathing_exercise.name}"

    class Meta:
        indexes = [
            models.Index(
                fields=["user", "started_at"],
                name="breath_user_started_idx",
            ),
            models.Index(
                fields=["breathing_exercise"],
                name="breath_exercise_idx",
            ),
        ]
