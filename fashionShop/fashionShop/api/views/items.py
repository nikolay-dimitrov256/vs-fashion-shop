from rest_framework.generics import ListAPIView

from fashionShop.api.serializers import ItemSerializer
from fashionShop.items.models import Item


class ItemsListView(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        items = Item.objects.active().with_main_picture()

        category = self.request.GET.get('category')
        colors = self.request.GET.getlist('color')
        sizes = self.request.GET.getlist('size')
        style = self.request.GET.get('style')
        search = self.request.GET.get('search', '').strip()

        if category:
            items = items.filter_category(category)

        if colors:
            items = items.filter_colors(colors)

        if sizes:
            items = items.filter_sizes(sizes)

        if style:
            items = items.filter(style__name__iexact=style)

        if search:
            items = items.search(search)

        return items.order_by('-is_new', 'collection__position', '-created_at').distinct()