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
        fields = ['pk', 'name_en', 'name_bg', 'slug', 'price', 'discount_price', 'is_new', 'color_group', 'pictures']