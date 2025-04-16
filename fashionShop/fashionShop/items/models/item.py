from datetime import datetime, timedelta

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from fashionShop.common.utils import transliterate
from fashionShop.items.models.categories import Category, SubCategory
from fashionShop.items.models.colors import ColorGroup
from fashionShop.items.models.pattern import Pattern
from fashionShop.items.models.size import Size
from fashionShop.items.models.style import Style


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

    is_bestseller = models.BooleanField(
        default=False,
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    sub_category = models.ForeignKey(
        to=SubCategory,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    pattern = models.ForeignKey(
        to=Pattern,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    color_group = models.ForeignKey(
        to=ColorGroup,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    sizes = models.ManyToManyField(
        to=Size,
        through='Stock',
        related_name='items'
    )

    linked_items = models.ManyToManyField(
        to='Item',
        blank=True,
    )

    style = models.ManyToManyField(
        to=Style,
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

    def get_available_sizes(self):
        available_sizes = Size.objects.filter(stock__item=self, stock__quantity__gt=0)

        return available_sizes.distinct()

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

    @property
    def final_price(self):
        if self.is_discounted:
            return self.discount_price

        return self.price

    def __str__(self):
        return str(self.item_number)


class Stock(models.Model):
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
    )

    store = models.ForeignKey(
        to='stores.Store',
        on_delete=models.CASCADE,
        default=0,
    )

    size = models.ForeignKey(
        to=Size,
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField(
        default=0
    )

    class Meta:
        unique_together = [['item', 'store', 'size']]
        verbose_name = _('stock')
        verbose_name_plural = _('stock')

    def __str__(self):
        return f'{str(self.item)} - {self.size.size}'
