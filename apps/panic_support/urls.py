from django.urls import path

from .views import (
    PanicGuideListView,
    PanicGuideDetailView,
    PanicCategoryListView,
    PanicCategoryGuideListView,
)

urlpatterns = [
    path(
        "guides/",
        PanicGuideListView.as_view(),
        name="panic_guide_list",
    ),
    path(
        "guides/<int:pk>/",
        PanicGuideDetailView.as_view(),
        name="panic_guide_detail",
    ),
    path(
        "categories/",
        PanicCategoryListView.as_view(),
        name="panic_category_list",
    ),
    path(
        "categories/<int:category_id>/guides/",
        PanicCategoryGuideListView.as_view(),
        name="panic_category_guides",
    ),
]