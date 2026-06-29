import datetime
import re

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from fashionShop.common.globals import FREE_DELIVERY_THRESHOLD
from fashionShop.common.utils import get_absolute_url
from fashionShop.sales.choices import ShippingChoices, StatusChoices, RefundStatusChoices

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
        max_length=20,
    )

    email = models.EmailField(
        _('e-mail'),
        max_length=50,
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
        # _('town'),
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

    status = models.CharField(
        max_length=3,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        blank=True,
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
    )

    bisoft_report_sent = models.BooleanField(
        default=False,
    )

    send_message = models.BooleanField(
        default=True,
    )

    ip = models.ForeignKey(
        to='accounts.IpAddress',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ['-pk'] # TODO: This causes problems in the order_code generation
        verbose_name = _('Online Order')
        verbose_name_plural = _('Online Orders')

    def save(self, *args, **kwargs):
        if not self.order_code:
            now = timezone.now()
            year = now.strftime('%y')
            month = now.strftime('%m')
            transaction_type = '49'
            start_of_month = timezone.make_aware(datetime.datetime(now.year, now.month, 1))
            last_order_this_month = OnlineOrder.objects.filter(created_at__gte=start_of_month).order_by('pk').last()

            if last_order_this_month and last_order_this_month.order_code:
                sequence = int(str(last_order_this_month.order_code[-4:])) + 1
            else:
                sequence = 1

            self.order_code = f'{year}{month}{transaction_type}{sequence:04d}'

        super().save(*args, **kwargs)

    @property
    def full_name(self):
        full_name = f'{self.first_name or ""} {self.last_name or ""}'

        if full_name.strip():
            return full_name.strip()

        return None

    @property
    def status_message(self) -> str | None:
        STATUS_SMS_TEMPLATES = {
            StatusChoices.PENDING: f'Вили Стил: Вашата поръчка е приета с номер {self.order_code}.',
            StatusChoices.SENT: f'Вили Стил: Поръчката Ви {self.order_code} беше предадена на куриер.',
            StatusChoices.COMPLETED: f'Вили Стил: Поръчката Ви {self.order_code} беше изпълнена. Ако сте доволни '
                                     f'от нея, ще се радваме да ни оставите положителен отзив:\n'
                                     f'{"\n".join(
                                         get_absolute_url("item-details", kwargs={"slug": slug})
                                         for slug in {oi.item.slug for oi in self.order_items.all()}
                                     )}',
        }

        message = STATUS_SMS_TEMPLATES.get(self.status)

        return message

    @property
    def infobip_phone(self) -> str:
        raw_phone = self.phone.replace(' ', '').replace('-', '')
        pattern = r'\(?\+?(359)?\)?0?(?P<phone>\d{9})\b'
        match = re.search(pattern, raw_phone)

        if match:
            phone = match.group('phone')

            cleaned_phone = f'359{phone}'

            return cleaned_phone

        return ''

    @property
    def ip_is_suspicious(self):
        return self.ip.is_suspicious

    @property
    def ip_is_banned(self):
        return self.ip.is_banned

    @property
    def admin_notification_message(self):
        order_string_as_list = ['Нова поръчка:']
        order_string_as_list += [
            f'{oi.item.pk} - {oi.item.name} - {oi.size.size} - {oi.quantity}бр. x {oi.at_price}€'
            for oi in self.order_items.all()
        ]
        order_string_as_list.append(f'Общо: {self.total}€')

        if self.total > FREE_DELIVERY_THRESHOLD.get('EUR'):
            order_string_as_list.append('За наша сметка')

        order_string_as_list.append(self.phone)

        if self.full_name:
            order_string_as_list.append(self.full_name)

        if self.shipping_method:
            order_string_as_list.append(self.get_shipping_method_display())

        office_choices = [ShippingChoices.SPEEDY_OFFICE, ShippingChoices.ECONT_OFFICE]
        address_choices = [ShippingChoices.SPEEDY_ADDRESS, ShippingChoices.ECONT_ADDRESS]

        if self.shipping_method in office_choices:
            order_string_as_list.append(self.office)
        elif self.shipping_method in address_choices:
            order_string_as_list.append(str(self.address))

        return '\n'.join(order_string_as_list)

    def __str__(self):
        return f'Order number {self.pk}'


class OnlineRefund(models.Model):
    order = models.ForeignKey(
        to=OnlineOrder,
        related_name='refunds',
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        max_length=3,
        choices=RefundStatusChoices.choices,
        default=RefundStatusChoices.PENDING,
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
    )

    refund_all = models.BooleanField(
        _('refund_all'),
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = _('Online Refund')
        verbose_name_plural = _('Online Refunds')

    def __str__(self):
        return f'{_('Refund for order')} {self.order.pk}'