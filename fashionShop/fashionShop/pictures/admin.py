from django.contrib import admin
from django.utils.html import format_html

from fashionShop.pictures.models import Picture


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ['item__item_number', 'image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="100" height="auto"/>')
        return 'No image'

    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'


class PictureInline(admin.StackedInline):
    model = Picture
    can_delete = True
    extra = 1
    fields = ['image', 'image_preview', 'is_main', 'is_detail', 'description_bg', 'description_en']
    readonly_fields = ['image_preview', 'created_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="100" height="auto"/>')
        return 'No image'

    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'
