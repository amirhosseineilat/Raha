from django.db import models
from django.db.models import Q, F


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=255)
    overview = models.TextField()
    content = models.TextField()

    picture = models.URLField(blank=True)

    article_category = models.ForeignKey(
        ArticleCategory, on_delete=models.PROTECT, related_name="articles"
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=100,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["status", "-published_at"],
                name="article_status_pub_idx",
            )
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(status="draft", published_at__isnull=True)
                | Q(status__in=["published", "archived"], published_at__isnull=False),
                name="article_status_publication_date_valid",
            )
        ]
