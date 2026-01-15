from django.contrib import admin

from fashionShop.common.models import Address, Feedback, ContactMessage


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'phone', 'created_at', 'message']