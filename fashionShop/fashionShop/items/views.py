from django.shortcuts import render
from django.views.generic import DetailView

from fashionShop.items.models import Item


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/single.html'

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        item.main_picture = item.pictures.first()

        return item
