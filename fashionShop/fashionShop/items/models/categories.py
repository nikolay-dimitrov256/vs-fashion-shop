from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(
        _('name'),
        max_length=20,
        blank=True
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(
        _('name'),
        max_length=50,
        blank=True
    )

    category = models.ForeignKey(
        verbose_name=_('category'),
        to=Category,
        on_delete=models.CASCADE,
        related_name='sub_categories',
    )

    class Meta:
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategories')
        ordering = ['name']

    def __str__(self):
        return self.name
