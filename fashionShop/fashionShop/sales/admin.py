from django.contrib import admin
from django.db.models import Count, Avg, Sum, Q
from django.db.models.functions import TruncMonth

from fashionShop.items.models import OrderItem
from fashionShop.sales.choices import StatusChoices
from fashionShop.sales.models import OnlineOrder
from fashionShop.sales.utils import refresh_orders


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ['item', 'size', 'quantity', 'at_price']


@admin.register(OnlineOrder)
class OnlineOrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ['order_code', 'full_name', 'phone', 'user', 'email',
                       'shipping_method', 'office', 'town', 'address', 'total',
                       'created_at', 'updated_at']
    search_fields = ['pk', 'order_code', 'first_name', 'last_name', 'comment', 'phone', 'email']
    list_filter = ['status', 'created_at']
    list_display = ['pk', 'full_name', 'status', 'total']
    change_list_template = 'admin/orders_changelist.html'
    actions = [refresh_orders]

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
                revenue=Sum('order_items__total_price', filter=Q(status=StatusChoices.COMPLETED))
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
