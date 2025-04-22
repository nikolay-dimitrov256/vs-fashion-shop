from django.contrib.auth import get_user_model
from django.db import models

from fashionShop.sales.choices import ShippingChoices

UserModel = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'{self.user.email}\'s Cart'


class OnlineOrder(models.Model):
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    phone = models.CharField(
        max_length=15,
    )

    email = models.EmailField(
        max_length=30,
        null=True,
        blank=True,
    )

    shipping_method = models.CharField(
        max_length=5,
        choices=ShippingChoices.choices,
        null=True,
        blank=True,
    )

    address = models.ForeignKey(
        to='common.Address',
        related_name='online_orders',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    @property
    def total(self):
        total = sum(item.total_price for item in self.order_items.all())

        return total

    def __str__(self):
        return f'Order number {self.pk}'
