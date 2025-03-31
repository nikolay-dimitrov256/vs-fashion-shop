from pprint import pprint

from django.db.models import OuterRef, Subquery, Prefetch
from django.shortcuts import render
from django.views.generic import DetailView

from fashionShop.items.models import Item
from fashionShop.pictures.models import Picture


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/single.html'

    def get_object(self, queryset=None):
        #item = super().get_object(queryset)
        item = (
            Item.objects
            .select_related('category', 'sub_category', 'pattern', 'color_group')
            .prefetch_related(
                'sizes',
                'linked_items',
                'linked_items__pictures',
                'pictures',
                # Prefetch(
                #     'pattern__items',
                #     queryset=Item.objects.exclude(pk=self.kwargs['pk']),
                #     to_attr='other_colors'
                # )
            )
            .get(pk=self.kwargs['pk'])
        )

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
            .select_related('pattern')
            .prefetch_related('pictures')
            .filter(pattern=self.object.pattern)
            .exclude(item_number=self.object.item_number)
        )

        return context
