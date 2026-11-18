from django.urls import path

from .views import (
    NotificationSettingsView,
    NotificationPreferenceListView,
    NotificationPreferenceUpdateView,
    NotificationLogListView,
)

urlpatterns = [
    path(
        "settings/",
        NotificationSettingsView.as_view(),
        name="notification_settings",
    ),
    path(
        "preferences/",
        NotificationPreferenceListView.as_view(),
        name="notification_preferences",
    ),
    path(
        "preferences/<int:pk>/",
        NotificationPreferenceUpdateView.as_view(),
        name="notification_preference_update",
    ),
    path(
        "history/",
        NotificationLogListView.as_view(),
        name="notification_history",
    ),
]