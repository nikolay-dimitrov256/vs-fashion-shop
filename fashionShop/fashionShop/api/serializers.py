from rest_framework import serializers

from fashionShop.items.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['pk', 'name_en', 'name_bg', 'slug', 'price', 'discount_price', 'is_new', 'color_group']