from django.contrib import admin
from .models import MoodFactor, DailyActivity, Mood, MoodEntryFactor, MoodEntryActivity


@admin.register(MoodFactor)
class MoodFactorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active"]


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active"]


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "score",
        "stress_level",
        "sleep_quality",
        "description",
        "date",
        "created_at",
        "updated_at",
    ]


@admin.register(MoodEntryFactor)
class MoodEntryFactorAdmin(admin.ModelAdmin):
    list_display = ["id", "mood", "factor"]


@admin.register(MoodEntryActivity)
class MoodEntryActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "mood", "activity"]
