from django.db import models

from fashionShop.items.models import Item, Size
from fashionShop.sales.models import OnlineOrder


class CartItem(models.Model):
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        related_name='cart_items',
    )

    cart = models.ForeignKey(
        to='sales.Cart',
        on_delete=models.CASCADE,
        related_name='cart_items',
    )

    size = models.ForeignKey(
        to=Size,
        on_delete=models.CASCADE,
        related_name='cart_items',
    )

    quantity = models.IntegerField(
        default=1,
    )

    @property
    def total_price(self):
        return self.item.final_price * self.quantity


class OrderItem(models.Model):
    item = models.ForeignKey(
        to=Item,
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    order = models.ForeignKey(
        to=OnlineOrder,
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    size = models.ForeignKey(
        to=Size,
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    at_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    @property
    def total_price(self):
        return self.at_price * self.quantity

    def __str__(self):
        return self.item.name
