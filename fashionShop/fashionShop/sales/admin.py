from django.contrib import admin

from fashionShop.items.models import OrderItem
from fashionShop.sales.models import OnlineOrder


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ['item', 'size', 'quantity', 'at_price']


@admin.register(OnlineOrder)
class OnlineOrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ['order_code', 'first_name', 'last_name', 'phone', 'user', 'email',
                       'shipping_method', 'office', 'town', 'address', 'total', 'comment',
                       'created_at', 'updated_at']
    search_fields = ['pk', 'order_code']
    list_filter = ['created_at']
    list_display = ['pk', 'status', 'total']
