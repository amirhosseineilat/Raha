from django.db import models
from django.db.models import Q, F
from django.conf import settings


class GameCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    class GameType(models.TextChoices):
        INTERNAL = "internal", "Internal"
        EXTERNAL = "external", "External"

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    thumbnail = models.URLField(blank=True)

    game_type = models.CharField(
        max_length=50, choices=GameType.choices, default=GameType.INTERNAL
    )
    game_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    game_categories = models.ManyToManyField(
        GameCategory, through="GameCategoryRelation", related_name="games"
    )

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(game_type="internal", game_url="")
                    | Q(game_type="external", game_url__gt="")
                ),
                name="game_type_url_valid",
            )
        ]


class GameCategoryRelation(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="game_category_relations"
    )

    game_category = models.ForeignKey(
        GameCategory, on_delete=models.CASCADE, related_name="game_relations"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['game','game_category'],
                name='unique_game_category'
            )
        ]

class GameSession(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"
        INTERRUPTED = "interrupted", "Interrupted"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_sessions"
    )

    game = models.ForeignKey(
        Game, on_delete=models.PROTECT, related_name="game_sessions"
    )

    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.IN_PROGRESS
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["user", "started_at"], name="started_at_game_session_idx"
            )
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(
                        status="in_progress",
                        ended_at__isnull=True,
                    )
                    | (
                        Q(
                            status__in=["completed", "abandoned", "interrupted"],
                            ended_at__isnull=False,
                        )
                        & Q(ended_at__gte=F("started_at"))
                    )
                ),
                name="game_session_valid_status_and_time",
            )
        ]
