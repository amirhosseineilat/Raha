from django.contrib import admin
from .models import GameCategory, Game, GameCategoryRelation, GameSession


@admin.register(GameCategory)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "is_active"]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
        "description",
        "thumbnail",
        "game_type",
        "game_url",
        "is_active",
        "created_at",
    ]


@admin.register(GameCategoryRelation)
class GameCategoryRelationAdmin(admin.ModelAdmin):
    list_display = ["id", "game", "game_category"]


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "game", "started_at", "ended_at", "status"]
