from django.contrib import admin
from django.db.models import Count, Avg, Sum, Q
from django.db.models.functions import TruncMonth

from fashionShop.items.models import OrderItem
from fashionShop.sales.choices import StatusChoices
from fashionShop.sales.models import OnlineOrder
from fashionShop.sales.tasks import send_sms
from fashionShop.sales.utils import refresh_orders, send_bisoft_reports


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ['item', 'quantity', 'at_price', 'total_price']


@admin.register(OnlineOrder)
class OnlineOrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ['order_code', 'full_name', 'phone', 'user', 'email',
                       'shipping_method', 'office', 'town', 'address', 'total',
                       'ip_is_suspicious', 'ip_is_banned', 'created_at', 'updated_at']
    search_fields = ['pk', 'order_code', 'first_name', 'last_name', 'comment', 'phone', 'email']
    list_filter = ['status', 'created_at']
    list_display = ['pk', 'order_code', 'full_name', 'status', 'total', 'bisoft_report_sent']
    change_list_template = 'admin/orders_changelist.html'
    actions = [refresh_orders, send_bisoft_reports]

    def changelist_view(self, request, extra_context=None):
        # Get the orders queryset
        qs = self.get_queryset(request)

        # Annotate by month
        monthly_data = (
            qs.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(
                total_orders=Count('pk'),
                avg_cart_value=Avg('total'),
                revenue=Sum('total', filter=Q(status=StatusChoices.COMPLETED)),
                pending=Count('pk', filter=Q(status=StatusChoices.PENDING)),
                confirmed=Count('pk', filter=Q(status=StatusChoices.CONFIRMED)),
                canceled=Count('pk', filter=Q(status=StatusChoices.CANCELED)),
                sent=Count('pk', filter=Q(status=StatusChoices.SENT)),
                rejected=Count('pk', filter=Q(status=StatusChoices.REJECTED)),
                abandoned=Count('pk', filter=Q(status=StatusChoices.ABANDONED)),
                completed=Count('pk', filter=Q(status=StatusChoices.COMPLETED)),
                replaced=Count('pk', filter=Q(status=StatusChoices.REPLACED)),
                refunded=Count('pk', filter=Q(status=StatusChoices.REFUNDED)),
                sklad=Sum('total', filter=Q(status=StatusChoices.COMPLETED) & Q(comment__icontains='Изпратена от склада')),
                pazardjik=Sum('total', filter=Q(status=StatusChoices.COMPLETED) & Q(comment__icontains='Изпратена от Пазарджик')),
                vazov=Sum('total', filter=Q(status=StatusChoices.COMPLETED) & Q(comment__icontains='Изпратена от Вазов')),
                vazov_refunded=Sum('total', filter=Q(status=StatusChoices.REFUNDED) & Q(comment__icontains='Изпратена от Вазов')),
                centar=Sum('total', filter=Q(status=StatusChoices.COMPLETED) & Q(comment__icontains='Изпратена от Център')),
                centar_refunded=Sum('total', filter=Q(status=StatusChoices.REFUNDED) & Q(comment__icontains='Изпратена от Център')),
                stara_zagora=Sum('total', filter=Q(status=StatusChoices.COMPLETED) & Q(comment__icontains='Изпратена от Стара Загора')),
                asenovgrad=Sum('total', filter=Q(status=StatusChoices.COMPLETED) & Q(comment__icontains='Изпратена от Асеновград')),
            )
            .order_by('-month')
        )

        # Breakdown by status
        raw_status_data = (
            qs.values('status')
            .annotate(count=Count('pk'))
        )

        # Convert codes to display names
        status_data = [
            {
                'status': dict(OnlineOrder._meta.get_field('status').choices).get(row['status'], row['status']),
                'count': row['count']
            }
            for row in raw_status_data
        ]

        extra_context = extra_context or {}
        extra_context['monthly_data'] = monthly_data
        extra_context['status_data'] = status_data

        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            # Fetch old status from DB before saving
            old_status = OnlineOrder.objects.only('status').get(pk=obj.pk).status

        # Save the object first
        super().save_model(request, obj, form, change)

        # If it’s a new order created from the admin
        if not change:
            if obj.status == StatusChoices.PENDING:
                send_sms(obj.infobip_phone, obj.status_message)
            return

        # For updates, check if status actually changed
        if old_status != obj.status and obj.send_message:
            send_sms(obj.infobip_phone, obj.status_message)
