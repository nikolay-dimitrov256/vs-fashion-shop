from datetime import timedelta, datetime

from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from fashionShop.common.utils import transliterate


class Item(models.Model):
    item_number = models.IntegerField(
        primary_key=True,
    )

    name = models.CharField(
        max_length=100,
        blank=True,
    )

    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    created_at = models.DateField(
        auto_now_add=True,
    )

    content = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        to='Category',
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    sub_category = models.ForeignKey(
        to='SubCategory',
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    pattern = models.ForeignKey(
        to='Pattern',
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    color_group = models.ForeignKey(
        to='ColorGroup',
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    sizes = models.ManyToManyField(
        to='Size',
        through='Stock',
        related_name='items'
    )

    linked_items = models.ManyToManyField(
        to='Item',
        blank=True,
    )

    style = models.ManyToManyField(
        to='Style',
        blank=True,
    )

    deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.item_number}-{transliterate(self.name_bg)}')

        if self.sub_category:
            self.category = self.sub_category.category

        super().save(*args, **kwargs)

    @property
    def is_discounted(self):
        if self.discount_price and 0 < self.discount_price < self.price:
            return True

        return False

    @property
    def is_new(self):
        if datetime.today().date() - self.created_at < timedelta(days=90):
            return True

        return False

    @property
    def discount(self):
        if not self.discount_price:
            return None

        return int(self.price - self.discount_price)

    def __str__(self):
        return str(self.item_number)


class Size(models.Model):
    size = models.CharField(
        max_length=15,
        primary_key=True,
    )

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = _('size')
        verbose_name_plural = _('sizes')
        ordering = ['size']


class Stock(models.Model):
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
    )

    size = models.ForeignKey(
        to=Size,
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField(
        default=0
    )

    class Meta:
        unique_together = [['item', 'size']]
        verbose_name = _('stock')
        verbose_name_plural = _('stock')

    def __str__(self):
        return str(self.item)


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


class Pattern(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = _('pattern')
        verbose_name_plural = _('patterns')

    def __str__(self):
        return self.name


class ColorGroup(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
    )

    color_code = models.CharField(
        max_length=10,
    )

    class Meta:
        verbose_name = _('color group')
        verbose_name_plural = _('color groups')

    def __str__(self):
        return self.name


class Style(models.Model):
    name = models.CharField(
        max_length=20,
    )

    class Meta:
        verbose_name = _('style')
        verbose_name_plural = _('styles')

    def __str__(self):
        return self.name
