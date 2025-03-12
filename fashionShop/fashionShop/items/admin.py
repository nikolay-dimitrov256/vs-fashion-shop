from django.contrib import admin

from fashionShop.items.models import Item, Category, SubCategory


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass
