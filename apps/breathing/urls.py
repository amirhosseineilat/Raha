from django.urls import path

from .views import (
    BreathingExerciseView,
    BreathingExerciseDetailView,
    BreathingSessionStartView,
    BreathingSessionFinishView,
    BreathingSessionFeedbackView,
    BreathingSessionListView,
)

urlpatterns = [
    path(
        "exercises/",
        BreathingExerciseView.as_view(),
        name="breathing_exercises",
    ),
    path(
        "exercises/<int:pk>/",
        BreathingExerciseDetailView.as_view(),
        name="breathing_exercise_detail",
    ),
    path(
        "session/start/",
        BreathingSessionStartView.as_view(),
        name="breathing_session_start",
    ),
    path(
        "session/finish/",
        BreathingSessionFinishView.as_view(),
        name="breathing_session_finish",
    ),
    path(
        "session/feedback/",
        BreathingSessionFeedbackView.as_view(),
        name="breathing_session_feedback",
    ),
    path(
        "sessions/",
        BreathingSessionListView.as_view(),
        name="breathing_session_list",
    ),
]