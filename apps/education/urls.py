from django.urls import path

from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCategoryListView,
    CategoryArticleListView,
)

urlpatterns = [
    path(
        "articles/",
        ArticleListView.as_view(),
        name="article_list",
    ),
    path(
        "articles/<int:pk>/",
        ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "categories/",
        ArticleCategoryListView.as_view(),
        name="article_categories",
    ),
    path(
        "categories/<int:category_id>/articles/",
        CategoryArticleListView.as_view(),
        name="category_articles",
    ),
]