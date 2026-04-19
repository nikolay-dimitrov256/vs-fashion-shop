from rest_framework.generics import ListAPIView

from fashionShop.api.serializers import ItemSerializer
from fashionShop.items.models import Item


class ItemsListView(ListAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()