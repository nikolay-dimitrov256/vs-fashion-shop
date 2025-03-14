from pprint import pprint

from django.contrib import admin
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
import requests

from fashionShop.items.models import Item, Category, SubCategory, Style, Size, Stock
from fashionShop.items.utils import parse_and_save_items, update_prices_and_stock
from fashionShop.settings import BISOFT_API_URL


class StockInline(admin.StackedInline):
    model = Stock
    fields = ['size', 'quantity']
    ordering = ['size__size']
    readonly_fields = ['size']
    can_delete = False


@admin.register(Item)
class ItemAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ['item_number', 'name', 'price', 'discount_price']
    list_filter = ['category']
    ordering = ['item_number']
    inlines = [StockInline]
    readonly_fields = ['slug']

    @button(visible=lambda self: self.context["request"].user.is_superuser,
            change_form=True,
            html_attrs={'style': 'background-color:#88FF88;color:black'})
    def load_items(self, request):
        response = requests.get(f'{BISOFT_API_URL}items/initial-items')
        data = response.json()

        parse_and_save_items(data)

        self.message_user(request, 'items loaded')
        # Optional: returns HttpResponse
        return HttpResponseRedirectToReferrer(request)

    @button(visible=lambda self: self.context["request"].user.is_superuser,
            change_form=True,
            html_attrs={'style': 'background-color:#88FF88;color:black'})
    def _update_prices_and_stock(self, request):

        update_prices_and_stock()

        self.message_user(request, 'items updated')

        return HttpResponseRedirectToReferrer(request)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


# @admin.register(Stock)
# class StockAdmin(admin.ModelAdmin):
#     list_display = ['item__item_number', 'size__size', 'quantity']
#     ordering = ['item__item_number', 'size__size']
#     search_fields = ['item__item_number']
#     readonly_fields = ['size']


