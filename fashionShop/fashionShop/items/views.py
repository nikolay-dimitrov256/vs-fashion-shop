from datetime import datetime, timedelta

from django.db.models import OuterRef, Subquery, Prefetch, Q, Avg, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from fashionShop.items.models import Item, ColorGroup, Stock, Size, SubCategory
from fashionShop.pictures.forms import ReviewPictureFormSet
from fashionShop.pictures.models import Picture
from fashionShop.reviews.forms import ReviewCreateForm


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/single.html'

    def get_object(self, queryset=None):
        # item = super().get_object(queryset)
        item = get_object_or_404(
            Item.objects
            .annotate(review_avg=Avg('reviews__rating'))
            .select_related('category', 'sub_category', 'pattern', 'color_group')
            .prefetch_related(
                'linked_items',
                'linked_items__pictures',
                'pictures',
                'reviews',
                'reviews__pictures'
            ),
            slug=self.kwargs['slug']
        )

        item.detail_pictures = item.pictures.filter(is_detail=True)
        if item.description:
            item.description = item.description.split(';')
            if len(item.description) == 1:
                item.description = item.description[0].split('\n')

        item.additional_info = item.additional_info.split(';') if item.additional_info else []

        return item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['available_sizes'] = (
            Stock.objects
            .filter(item=self.object, quantity__gt=0)
            .annotate(effective_size=Coalesce('translated_size', 'size'))
            .values_list('effective_size', flat=True)
            .order_by('size__size')
            .distinct()
        )
        context['other_colors'] = (
            Item.objects
            .exclude(Q(deleted=True) | Q(pk=self.object.pk))
            .filter(pattern=self.object.pattern, pattern__isnull=False)
        )
        context['review_avg'] = round(self.object.review_avg or 0)
        context['review_form'] = ReviewCreateForm(self.request.POST or None)
        context['formset'] = ReviewPictureFormSet(self.request.POST or None, self.request.FILES or None)

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
                Q(stock__translated_size__size__in=selected_sizes) |
                Q(stock__translated_size__isnull=True, stock__size__size__in=selected_sizes),
                stock__quantity__gt=0,
            )

        return items.order_by('-created_at').distinct()

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


class TankTopsListView(ItemsListView):
    template_name = 'items/tank-tops.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='underwear')

        return items


class SetsListView(ItemsListView):
    template_name = 'items/sets.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='classic')

        return items


class CardigansListView(ItemsListView):
    template_name = 'items/tank-tops.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='cardigans')

        return items


class ElegantListView(ItemsListView):
    template_name = 'items/elegant.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(style__name__iexact='elegant')

        return items


class OfficeListView(ItemsListView):
    template_name = 'items/office.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(style__name__iexact='office')

        return items


class OfficialListView(ItemsListView):
    template_name = 'items/official.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(style__name__iexact='official')

        return items


class SearchView(ItemsListView):
    template_name = 'items/search.html'

    def get_queryset(self):
        items = super().get_queryset()

        search = self.request.GET.get('search', '').strip()
        query = (Q(name__icontains=search) | Q(name_en__icontains=search)
                 | Q(description__icontains=search) | Q(description_en__icontains=search))

        if search.isdigit():
            query |= Q(pk=search)

        items = items.filter(query)

        return items


class BestsellersListView(ItemsListView):
    template_name = 'items/bestsellers.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.annotate(sales=Sum('order_items__quantity')).filter(sales__gte=5).order_by('-sales')

        return items


class NewItemsListView(ItemsListView):
    template_name = 'items/new.html'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(created_at__gte=datetime.today().date() - timedelta(days=60)).order_by('-created_at')

        return items
