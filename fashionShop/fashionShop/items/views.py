from pprint import pprint

from django.db.models import OuterRef, Subquery, Prefetch, Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from fashionShop.items.models import Item, ColorGroup, Stock, Size, SubCategory
from fashionShop.pictures.models import Picture


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/single.html'

    def get_object(self, queryset=None):
        # item = super().get_object(queryset)
        item = get_object_or_404(
            Item.objects
            .select_related('category', 'sub_category', 'pattern', 'color_group')
            .prefetch_related(
                'linked_items',
                'linked_items__pictures',
                'pictures',
                Prefetch(
                    'pattern__items',
                    queryset=Item.objects.exclude(Q(slug=self.kwargs['slug']) | Q(deleted=True)),
                    to_attr='other_colors'
                )
            ),
            slug=self.kwargs['slug']
        )

        item.detail_pictures = item.pictures.filter(is_detail=True)
        if item.description:
            item.description = item.description.split(';')
            if len(item.description) == 1:
                item.description = item.description[0].split('\n')

        return item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['available_sizes'] = (
            Stock.objects
            .filter(item=self.object, quantity__gt=0)
            .values_list('size', flat=True)
            .distinct()
        )

        return context


class ItemsListView(ListView):
    model = Item
    template_name = 'items/category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        context['colors'] = ColorGroup.objects.all()
        context['sizes'] = Stock.objects.values_list('size', flat=True).order_by('size').distinct()
        context['paginate_by'] = self.get_paginate_by(self.queryset)

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = query_params

        return context

    def get_queryset(self):
        items = (
            Item.objects
            .prefetch_related(
                Prefetch(
                    'pictures',
                    queryset=Picture.objects.all()[:1],  # Only fetch the first image
                    to_attr='main_picture_list'
                )
            )
            .exclude(deleted=True)
        )

        selected_colors = self.request.GET.getlist('color')
        if selected_colors:
            items = items.filter(color_group__name_en__in=selected_colors)

        selected_sizes = self.request.GET.getlist('size')
        if selected_sizes:
            items = items.filter(
                stock__quantity__gt=0,
                stock__size__size__in=selected_sizes
            )

        return items

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('show', 12)

        return paginate_by


class PantsListView(ItemsListView):
    template_name = 'items/pants.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='pants')

        return items


class SkirtsListView(ItemsListView):
    template_name = 'items/skirts.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='skirts')

        return items


class DressesListView(ItemsListView):
    template_name = 'items/dresses.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='dresses')

        return items


class ShirtsListView(ItemsListView):
    template_name = 'items/shirts.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='shirts')

        return items


class BlousesListView(ItemsListView):
    template_name = 'items/blouses.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='blouses')

        return items


class TunicsListView(ItemsListView):
    template_name = 'items/tunics.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='tunics')

        return items


class BlazersListView(ItemsListView):
    template_name = 'items/blazers.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='blazers')

        return items


class SuitsListView(ItemsListView):
    template_name = 'items/suits.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='suits')

        return items


class JacketsListView(ItemsListView):
    template_name = 'items/jackets.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='jackets')

        return items


class CoatsListView(ItemsListView):
    template_name = 'items/coats.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='coats')

        return items


class VestsListView(ItemsListView):
    template_name = 'items/vests.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='vests')

        return items
