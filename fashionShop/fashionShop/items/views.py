from django.db.models import OuterRef, Subquery
from django.shortcuts import render
from django.views.generic import DetailView

from fashionShop.items.models import Item
from fashionShop.pictures.models import Picture


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/single.html'

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        item.main_picture = item.pictures.first()
        item.detail_pictures = item.pictures.filter(is_detail=True)
        if item.description:
            item.description = item.description.split(';')
            if len(item.description) == 1:
                item.description = item.description[0].split('\n')

        return item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['other_colors'] = (
            Item.objects
            .filter(pattern=self.object.pattern)
            .exclude(item_number=self.object.item_number)
        )

        return context
