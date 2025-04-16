from django.db import models

from fashionShop.items.models import Item, Size


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
