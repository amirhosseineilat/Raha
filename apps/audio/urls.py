from django.urls import path
from .views import AudioSessionView, AudioContentView, AudioCategoryView

urlpatterns = [
    path("audio_content/", AudioContentView.as_view(), name="audio-content"),
    path("audio_category/", AudioCategoryView.as_view(), name="audio-category"),
    path("session/", AudioSessionView.as_view(), name="audio-session"),
]
