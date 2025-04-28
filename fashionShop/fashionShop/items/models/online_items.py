from django.db import models
from django.utils.translation import gettext_lazy as _

from fashionShop.items.models import Item, Size
from fashionShop.sales.models import OnlineOrder


class CartItem(models.Model):
    item = models.ForeignKey(
        verbose_name=_('item'),
        to=Item,
        on_delete=models.CASCADE,
        related_name='cart_items',
    )

    cart = models.ForeignKey(
        verbose_name=_('cart'),
        to='sales.Cart',
        on_delete=models.CASCADE,
        related_name='cart_items',
    )

    size = models.ForeignKey(
        verbose_name=_('size'),
        to=Size,
        on_delete=models.CASCADE,
        related_name='cart_items',
    )

    quantity = models.IntegerField(
        verbose_name=_('quantity'),
        default=1,
    )

    @property
    def total_price(self):
        return self.item.final_price * self.quantity


class OrderItem(models.Model):
    item = models.ForeignKey(
        verbose_name=_('item'),
        to=Item,
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    order = models.ForeignKey(
        verbose_name='order',
        to=OnlineOrder,
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    size = models.ForeignKey(
        verbose_name=_('size'),
        to=Size,
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    quantity = models.PositiveIntegerField(
        verbose_name=_('quantity'),
        default=1,
    )

    at_price = models.DecimalField(
        verbose_name=_('at price'),
        max_digits=10,
        decimal_places=2,
    )

    @property
    def total_price(self):
        return self.at_price * self.quantity

    def __str__(self):
        return self.item.name
