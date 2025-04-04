from pprint import pprint

from django.db.models import OuterRef, Subquery, Prefetch, Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from fashionShop.items.models import Item, ColorGroup, Stock, Size
from fashionShop.pictures.models import Picture


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/single.html'

    def get_object(self, queryset=None):
        # item = super().get_object(queryset)
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
            .get(slug=self.kwargs['slug'])
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


class ItemsListView(ListView):
    model = Item
    template_name = 'items/category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        context['colors'] = ColorGroup.objects.all()
        context['sizes'] = Size.objects.filter(items__isnull=False).values_list('size', flat=True).distinct()
        context['paginate_by'] = self.get_paginate_by(self.queryset)
        #context['available_colors'] = ColorGroup.objects.all()
        #context['color'] = self.request.GET.get('color', '')

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = query_params
        print(query_params)
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

        # color = self.request.GET.get('color', '')
        # if color:
        #     color_query = Q(color_group__name_en__icontains=color.lower().strip())
        #     items = items.filter(color_query)

        selected_colors = self.request.GET.getlist('color')
        if selected_colors:
            items = items.filter(color_group__name_en__in=selected_colors)

        selected_sizes = self.request.GET.getlist('size')
        if selected_sizes:
            items = items.filter(sizes__size__in=selected_sizes)

        return items

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('show', 12)

        return paginate_by
