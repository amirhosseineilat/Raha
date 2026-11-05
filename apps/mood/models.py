from django.db import models
from django.conf import settings
from django.db.models import Q

class MoodFactor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DailyActivity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Mood(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="moods")

    score = models.IntegerField()
    stress_level = models.IntegerField()
    sleep_quality = models.IntegerField()

    description = models.TextField(blank=True)

    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    factors = models.ManyToManyField(
        MoodFactor,
        through="MoodEntryFactor",
        related_name="moods",
    )

    activities = models.ManyToManyField(
        DailyActivity,
        through="MoodEntryActivity",
        related_name="moods",
    )

    def __str__(self):
        return f"{self.user.email} - {self.date}"

    class Meta:

        constraints = [
            models.CheckConstraint(
                condition=Q(score__gte=1) & Q(score__lte=5),
                name="mood_score_between_1_and_5",
            ),
            models.CheckConstraint(
                condition=Q(stress_level__gte=1) & Q(stress_level__lte=5),
                name="mood_stress_between_1_and_5",
            ),
            models.CheckConstraint(
                condition=Q(sleep_quality__gte=1) & Q(sleep_quality__lte=5),
                name="mood_sleep_between_1_and_5",
            ),
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_mood_per_user_per_day",
            ),
        ]


class MoodEntryFactor(models.Model):
    mood = models.ForeignKey(
        Mood,
        on_delete=models.CASCADE,
    )

    factor = models.ForeignKey(
        MoodFactor,
        on_delete=models.PROTECT,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["mood", "factor"],
                name="unique_mood_factor",
            ),
        ]


class MoodEntryActivity(models.Model):
    mood = models.ForeignKey(
        Mood,
        on_delete=models.CASCADE,
    )

    activity = models.ForeignKey(
        DailyActivity,
        on_delete=models.PROTECT,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["mood", "activity"],
                name="unique_mood_activity",
            ),
        ]
