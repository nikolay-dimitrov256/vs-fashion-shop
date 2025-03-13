from pprint import pprint

from django.contrib import admin
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
import requests

from fashionShop.items.models import Item, Category, SubCategory, Style
from fashionShop.items.utils import parse_and_save_items


@admin.register(Item)
class ItemAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    @button(visible=lambda self: self.context["request"].user.is_superuser,
            change_form=True,
            html_attrs={'style': 'background-color:#88FF88;color:black'})
    def load_items(self, request):
        response = requests.get('http://127.0.0.1:8001/items/initial-items')
        data = response.json()

        parse_and_save_items(data)

        self.message_user(request, 'items loaded')
        # Optional: returns HttpResponse
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
