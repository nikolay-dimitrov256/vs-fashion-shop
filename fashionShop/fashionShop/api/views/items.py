from django.db.models import Prefetch
from rest_framework.generics import ListAPIView

from fashionShop.api.serializers import ItemSerializer
from fashionShop.items.models import Item
from fashionShop.pictures.models import Picture


class ItemsListView(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        color = self.request.GET.get('color')
        print(color)
        items = (
            Item.objects
                .prefetch_related('pictures')
                .exclude(deleted=True)
        )

        return items