from django.shortcuts import render


from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from .models import Article, ArticleCategory


class ArticleListView(ListView):
    model = Article
    template_name = "education/article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        return (
            Article.objects.filter(
                status=Article.Status.PUBLISHED,
                article_category__is_active=True,
            )
            .select_related("article_category")
            .order_by("-published_at")
        )


class ArticleDetailView(DetailView):
    model = Article
    template_name = "education/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return (
            Article.objects.filter(
                status=Article.Status.PUBLISHED,
                article_category__is_active=True,
            )
            .select_related("article_category")
        )


class ArticleCategoryListView(ListView):
    model = ArticleCategory
    template_name = "education/article_category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return ArticleCategory.objects.filter(
            is_active=True,
        ).order_by("name")


class CategoryArticleListView(ListView):
    model = Article
    template_name = "education/category_article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(
            ArticleCategory,
            pk=self.kwargs["category_id"],
            is_active=True,
        )

        return (
            Article.objects.filter(
                article_category=self.category,
                status=Article.Status.PUBLISHED,
            )
            .select_related("article_category")
            .order_by("-published_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
