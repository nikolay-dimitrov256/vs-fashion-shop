from django.contrib import admin

from fashionShop.common.models import Address
from fashionShop.stores.models import Store


class AddressInline(admin.StackedInline):
    model = Address
    can_delete = False
    fields = ['country', 'province', 'town', 'postal_code', 'street', 'number', 'building', 'entrance', 'apartment']


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    inlines = [AddressInline]
