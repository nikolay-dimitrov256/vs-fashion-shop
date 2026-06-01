from fashionShop.sales.models import OnlineOrder
from fashionShop.sales.tasks import send_bisoft_report
from django.utils.translation import gettext_lazy as _


def refresh_orders(modeladmin, request, queryset):
    for order in queryset:
        for item in order.order_items.all():
            item.save()

        order.save()


refresh_orders.short_description = 'Refresh orders'


def send_bisoft_reports(modeladmin, request, queryset):
    orders = list(queryset)
    for order in orders:
        # if not order.bisoft_report_sent:
        success = send_bisoft_report(order.pk, save=False)
        order.bisoft_report_sent = success

    OnlineOrder.objects.bulk_update(orders, ['bisoft_report_sent'])


send_bisoft_reports.short_description = _('Send BiSOFT reports')