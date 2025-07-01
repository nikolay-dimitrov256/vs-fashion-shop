import time
from pprint import pprint

from django.contrib import admin
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
import requests

from fashionShop.items.models import Item, Category, SubCategory, Style, Size, Stock, ColorGroup, Pattern
from fashionShop.items.tasks import load_items_from_bisoft
from fashionShop.items.utils import parse_and_save_items, update_prices_and_stock
from fashionShop.pictures.admin import PictureInline


class StockInline(admin.TabularInline):
    model = Stock
    fields = ['size', 'translated_size', 'quantity']
    ordering = ['size__size']
    # readonly_fields = ['size']
    can_delete = False


@admin.register(Item)
class ItemAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ['item_number', 'name', 'price', 'discount_price']
    list_filter = ['category', 'style', 'color_group']
    ordering = ['item_number']
    inlines = [PictureInline, StockInline]
    readonly_fields = ['slug', 'created_at']
    search_fields = ['item_number', 'name']

    @button(visible=lambda self: self.context["request"].user.is_superuser,
            change_form=True,
            html_attrs={'style': 'background-color:#88FF88;color:black'})
    def load_items(self, request):
        start = time.time()

        load_items_from_bisoft()

        end = time.time()
        self.message_user(request, f'The operation took {end - start} seconds')

        # Optional: returns HttpResponse
        return HttpResponseRedirectToReferrer(request)

    @button(visible=lambda self: self.context["request"].user.is_superuser,
            change_form=True,
            html_attrs={'style': 'background-color:#88FF88;color:black'})
    def _update_prices_and_stock(self, request):

        # update_prices_and_stock()

        self.message_user(request, 'Function not available yet.')

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


@admin.register(ColorGroup)
class ColorGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    pass
