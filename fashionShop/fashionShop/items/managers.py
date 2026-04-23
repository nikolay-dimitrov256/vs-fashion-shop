from django.db import models
from django.db.models import Prefetch, Q, Sum
from fashionShop.pictures.models import Picture

class ItemQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(deleted=True)

    def with_main_picture(self):
        return self.prefetch_related(
            Prefetch(
                'pictures',
                queryset=Picture.objects.all()[:1],
                to_attr='main_picture_list'
            )
        )

    def filter_colors(self, colors: list):
        if colors:
            return self.filter(color_group__name_en__in=colors)
        return self

    def filter_sizes(self, sizes: list):
        if sizes:
            return self.filter(
                Q(stock__translated_size__size__in=sizes) |
                Q(stock__translated_size__isnull=True, stock__size__size__in=sizes),
                stock__quantity__gt=0,
            )
        return self

    def filter_category(self, category: str):
        if category:
            return self.filter(category__name_en=category)
        return self

    def search(self, search: str):
        if search:
            query = (Q(name__icontains=search) | Q(name_en__icontains=search)
                     | Q(description__icontains=search) | Q(description_en__icontains=search))

            if search.isdigit():
                query |= Q(pk=search)

            return self.filter(query)
        return self

    def bestsellers(self):
        return self.annotate(sales=Sum('order_items__quantity')).filter(sales__gte=5).order_by('-sales')

    def max_sizes(self):
        max_sizes = ['52', '54', '56', '58', '60', '62', '64', '66', '68', '70']

        query = (
            Q(stock__translated_size__size__in=max_sizes) |
            Q(stock__translated_size__size__isnull=True, stock__size__size__in=max_sizes)
        ) & Q(stock__quantity__gt=0)

        return self.filter(query)

    def fall_winter(self):
        query = Q(collection__name='есен/зима') | Q(collection__name='пролет/есен')

        return self.filter(query)

    def spring_summer(self):
        query = Q(collection__name='пролет/лято') | Q(collection__name='пролет/есен') | Q(collection__name='лято')

        return self.filter(query)


class ItemManager(models.Manager.from_queryset(ItemQuerySet)):
    pass