
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from .models import PanicGuide, PanicCategory


class PanicGuideListView(ListView):
    model = PanicGuide
    template_name = "panic_support/panic_guide_list.html"
    context_object_name = "panic_guides"
    paginate_by = 10

    def get_queryset(self):
        return (
            PanicGuide.objects.filter(is_active=True)
            .prefetch_related("categories")
        )


class PanicGuideDetailView(DetailView):
    model = PanicGuide
    template_name = "panic_support/panic_guide_detail.html"
    context_object_name = "panic_guide"

    def get_queryset(self):
        return (
            PanicGuide.objects.filter(is_active=True)
            .prefetch_related("categories")
        )


class PanicCategoryListView(ListView):
    model = PanicCategory
    template_name = "panic_support/panic_category_list.html"
    context_object_name = "panic_categories"

    def get_queryset(self):
        return PanicCategory.objects.all().order_by("name")


class PanicCategoryGuideListView(ListView):
    model = PanicGuide
    template_name = "panic_support/panic_category_guides.html"
    context_object_name = "panic_guides"
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(
            PanicCategory,
            pk=self.kwargs["category_id"],
        )

        return (
            PanicGuide.objects.filter(
                is_active=True,
                categories=self.category,
            )
            .prefetch_related("categories")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
