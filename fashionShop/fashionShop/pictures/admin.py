from django.contrib import admin
from django.utils.html import format_html

from fashionShop.pictures.models import Picture
from fashionShop.pictures.utils.cloudflare import migrate_image_to_r2


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ['item__item_number', 'image_preview', 'r2_status']
    actions = [migrate_image_to_r2]

    def image_preview(self, obj):
        if obj.image_r2 or obj.image:
            return format_html('<img src="{}" width="100" style="height:auto;"/>', obj.image_url)
        return 'No image'

    image_preview.short_description = 'Preview'

    def r2_status(self, obj):
        return '✅' if obj.image_r2 else '❌'

    r2_status.short_description = 'R2'


class PictureInline(admin.TabularInline):
    model = Picture
    can_delete = True
    extra = 1
    fields = ['image_r2', 'image_preview', 'is_main', 'is_detail', 'description_bg', 'description_en']
    readonly_fields = ['image_preview', 'created_at']

    def image_preview(self, obj):
        if obj.image_r2 or obj.image:
            return format_html('<img src="{}" width="100" style="height:auto;"/>', obj.image_url)
        return 'No image'

    image_preview.short_description = 'Preview'
