from django.contrib import admin
from .models import BreathingExercise, BreathingSession


@admin.register(BreathingExercise)
class BreathingExerciseAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "description",
        "inhale_time",
        "holding",
        "exhale",
        "guidance_audio",
        "animation_url",
    ]


@admin.register(BreathingSession)
class BreathingSessionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "breathing_exercise",
        "duration",
        "started_at",
        "ended_at",
        "status",
        "feedback",
        "feedback_note",
    ]
