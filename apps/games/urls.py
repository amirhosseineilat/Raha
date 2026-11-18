from django.urls import path

from .views import (
    GameListView,
    GameDetailView,
    GameCategoryListView,
    GameCategoryDetailView,
    GameSessionStartView,
    GameSessionFinishView,
)

urlpatterns = [
    path("", GameListView.as_view(), name="game_list"),
    path("categories/", GameCategoryListView.as_view(), name="game_category_list"),
    path(
        "categories/<int:category_id>/",
        GameCategoryDetailView.as_view(),
        name="game_category_detail",
    ),
    path(
        "sessions/finish/", GameSessionFinishView.as_view(), name="game_session_finish"
    ),
    path(
        "<slug:slug>/start/", GameSessionStartView.as_view(), name="game_session_start"
    ),
    path("<slug:slug>/", GameDetailView.as_view(), name="game_detail"),
]
