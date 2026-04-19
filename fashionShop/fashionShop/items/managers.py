from django.db import models
from django.db.models import Prefetch, Q
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