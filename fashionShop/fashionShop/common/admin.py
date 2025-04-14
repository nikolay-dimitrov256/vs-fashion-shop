from django.contrib import admin

from fashionShop.common.models import Address, Feedback


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass
