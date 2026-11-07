from django.contrib import admin
from .models import ArticleCategory,Article

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'overview', 'content', 'picture', 'article_category', 'published_at', 'status']