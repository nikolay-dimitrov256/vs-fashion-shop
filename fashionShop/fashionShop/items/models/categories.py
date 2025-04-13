from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(
        max_length=20,
        blank=True
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(
        max_length=50,
        blank=True
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='sub_categories',
    )

    class Meta:
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategories')

    def __str__(self):
        return self.name
