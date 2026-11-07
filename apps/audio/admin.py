from django.contrib import admin
from .models import AudioCategory, AudioContent, AudioSession


@admin.register(AudioCategory)
class AudioCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active"]


@admin.register(AudioContent)
class AudioContentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "sound", "audio_category"]


@admin.register(AudioSession)
class AudioSessionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "audio_content",
        "started_at",
        "ended_at",
        "last_position",
        "status",
    ]
