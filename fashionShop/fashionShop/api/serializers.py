from rest_framework import serializers

from fashionShop.items.models import Item
from fashionShop.pictures.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['image_url']


class ItemSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(read_only=True, many=True)

    class Meta:
        model = Item
        fields = [
            'pk', 'name', 'slug', 'price', 'price_bgn', 'discount_price', 'discount_price_bgn', 'is_new', 'discount',
            'pictures', 'is_discounted'
        ]