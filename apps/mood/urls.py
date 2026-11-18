from django.urls import path

from .views import (
    MoodListView,
    MoodDetailView,
    MoodCreateView,
    MoodUpdateView,
    MoodFactorListView,
    DailyActivityListView,
)

urlpatterns = [
    path("", MoodListView.as_view(), name="mood_list"),

    path("create/", MoodCreateView.as_view(), name="mood_create"),

    path("<int:pk>/", MoodDetailView.as_view(), name="mood_detail"),

    path("<int:pk>/update/", MoodUpdateView.as_view(), name="mood_update"),

    path("factors/", MoodFactorListView.as_view(), name="mood_factors"),

    path("activities/", DailyActivityListView.as_view(), name="daily_activities"),
]