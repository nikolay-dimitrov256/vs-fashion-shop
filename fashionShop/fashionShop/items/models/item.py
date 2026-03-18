from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from fashionShop.common.globals import EURO_RATE, black_friday_discount_percent, is_black_friday
from fashionShop.common.utils import transliterate
from fashionShop.items.models import ItemCollection
from fashionShop.items.models.categories import Category, SubCategory
from fashionShop.items.models.colors import ColorGroup
from fashionShop.items.models.pattern import Pattern
from fashionShop.items.models.size import Size
from fashionShop.items.models.style import Style


class Item(models.Model):
    item_number = models.IntegerField(
        _('item number'),
        primary_key=True,
    )

    name = models.CharField(
        _('name'),
        max_length=100,
        blank=True,
    )

    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
    )

    description = models.TextField(
        _('description'),
        null=True,
        blank=True,
    )

    additional_info = models.TextField(
        _('additional information'),
        null=True,
        blank=True,
    )

    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    discount_price = models.DecimalField(
        _('discount price'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    created_at = models.DateField(
        auto_now_add=True,
    )

    content = models.CharField(
        _('content'),
        max_length=100,
        null=True,
        blank=True,
    )

    is_bestseller = models.BooleanField(
        default=False,
    )

    is_new = models.BooleanField(
        default=False,
    )

    category = models.ForeignKey(
        verbose_name=_('category'),
        to=Category,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    sub_category = models.ForeignKey(
        verbose_name=_('subcategory'),
        to=SubCategory,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    pattern = models.ForeignKey(
        verbose_name=_('pattern'),
        to=Pattern,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    color_group = models.ForeignKey(
        verbose_name=_('color group'),
        to=ColorGroup,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    collection = models.ForeignKey(
        verbose_name=_('collection'),
        to=ItemCollection,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
        blank=True,
    )

    sizes = models.ManyToManyField(
        verbose_name=_('sizes'),
        to=Size,
        through='Stock',
        related_name='items',
        through_fields=('item', 'size'),
    )

    linked_items = models.ManyToManyField(
        verbose_name=_('linked items'),
        to='Item',
        blank=True,
    )

    style = models.ManyToManyField(
        verbose_name=_('style'),
        to=Style,
        blank=True,
    )

    deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.item_number}-{transliterate(self.name_bg)}')

        if self.sub_category:
            self.category = self.sub_category.category

        super().save(*args, **kwargs)

    def get_available_sizes(self):
        available_sizes = Size.objects.filter(stock__item=self, stock__quantity__gt=0)

        return available_sizes.distinct()

    @property
    def is_discounted(self) -> bool:
        if self.discount_price and 0 < self.discount_price < self.price:
            return True

        return False

    @property
    def discount(self) -> Decimal:
        if is_black_friday:
            return self.price - self.black_price

        if not self.is_discounted:
            return Decimal(0)

        return (self.price - self.discount_price).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    @property
    def discount_bgn(self) -> Decimal:
        return (self.discount * Decimal(EURO_RATE)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    @property
    def final_price(self) -> Decimal:
        if is_black_friday:
            return self.black_price

        if self.is_discounted:
            return self.discount_price

        return self.price

    @property
    def price_bgn(self) -> Decimal:
        return (self.price * Decimal(EURO_RATE)).quantize(Decimal('.01'))

    @property
    def discount_price_bgn(self) -> Decimal|None:
        if self.discount_price is None:
            return None
        return (self.discount_price * Decimal(EURO_RATE)).quantize(Decimal('.01'))

    @property
    def final_price_bgn(self) -> Decimal:
        if is_black_friday:
            return self.black_price_bgn

        if self.is_discounted:
            return self.discount_price_bgn

        return self.price_bgn

    @property
    def black_price(self) -> Decimal:
        price = self.discount_price if self.is_discounted else self.price
        discount = Decimal(black_friday_discount_percent / 100) * price
        black_price = price - discount

        return black_price.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    @property
    def black_price_bgn(self) -> Decimal:
        return (self.black_price * Decimal(EURO_RATE)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)



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

    translated_size = models.ForeignKey(
        to=Size,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='translated_sizes',
    )

    class Meta:
        unique_together = [['item', 'store', 'size']]
        verbose_name = _('stock')
        verbose_name_plural = _('stock')

    @property
    def effective_size(self):
        return self.translated_size or self.size

    def __str__(self):
        return f'{str(self.item)} - {self.effective_size.size}'
