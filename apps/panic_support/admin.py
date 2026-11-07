from django.contrib import admin
from .models import PanicCategory, PanicGuide, PanicGuideCategories


@admin.register(PanicCategory)
class PanicCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(PanicGuide)
class PanicGuideAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "is_active"]


@admin.register(PanicGuideCategories)
class PanicGuideCategoriesAdmin(admin.ModelAdmin):
    list_display = ["id", "panic_category", "panic_guide"]
