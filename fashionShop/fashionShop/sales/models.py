import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

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

    first_name = models.CharField(
        _('first name'),
        max_length=20,
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        _('last name'),
        max_length=20,
        null=True,
        blank=True,
    )

    phone = models.CharField(
        _('phone'),
        max_length=15,
    )

    email = models.EmailField(
        _('e-mail'),
        max_length=30,
        null=True,
        blank=True,
    )

    shipping_method = models.CharField(
        _('shipping method'),
        max_length=5,
        choices=ShippingChoices.choices,
        null=True,
        blank=True,
    )

    address = models.ForeignKey(
        to='common.Address',
        related_name='online_orders',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    town = models.CharField(
        _('town'),
        max_length=30,
        null=True,
        blank=True,
    )

    office = models.CharField(
        _('office'),
        max_length=100,
        null=True,
        blank=True,
    )

    comment = models.TextField(
        _('comment'),
        null=True,
        blank=True,
    )

    order_code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):
        if not self.order_code:
            now = timezone.now()
            year = now.strftime('%y')
            month = now.strftime('%m')
            transaction_type = '49'
            start_of_month = timezone.make_aware(datetime.datetime(now.year, now.month, 1))
            last_order_this_month = OnlineOrder.objects.filter(created_at__gte=start_of_month).last()

            if last_order_this_month and last_order_this_month.order_code:
                sequence = int(str(last_order_this_month.order_code[-4:])) + 1
            else:
                sequence = 1

            self.order_code = f'{year}{month}{transaction_type}{sequence:04d}'

        super().save(*args, **kwargs)

    @property
    def total(self):
        total = sum(item.total_price for item in self.order_items.all())

        return total

    def __str__(self):
        return f'Order number {self.pk}'
