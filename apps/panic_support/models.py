from django.db import models


class PanicCategory(models.Model):
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name


class PanicGuide(models.Model):
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(
        PanicCategory, through="PanicGuideCategories", related_name="panic_guides"
    )

    def __str__(self):
        return self.context


class PanicGuideCategories(models.Model):
    panic_category = models.ForeignKey(PanicCategory, on_delete=models.PROTECT)

    panic_guide = models.ForeignKey(PanicGuide, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["panic_category", "panic_guide"],
                name="unique_category_guide",
            ),
        ]
