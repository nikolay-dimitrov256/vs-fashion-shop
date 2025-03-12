from modeltranslation.translator import register, TranslationOptions

from fashionShop.items.models import Item, Category, SubCategory


@register(Item)
class ItemTranslationOptions(TranslationOptions):
    fields = ['name', 'description', 'content']


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['name']


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ['name']