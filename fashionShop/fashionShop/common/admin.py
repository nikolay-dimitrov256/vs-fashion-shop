from django.contrib import admin

from fashionShop.common.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
