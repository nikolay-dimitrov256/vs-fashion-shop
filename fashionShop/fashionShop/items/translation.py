from modeltranslation.translator import register, TranslationOptions

from fashionShop.items.models import Item, Category, SubCategory, ColorGroup


@register(Item)
class ItemTranslationOptions(TranslationOptions):
    fields = ['name', 'description', 'content', 'additional_info']


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['name']


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ['name']


@register(ColorGroup)
class ColorGroupTranslationOptions(TranslationOptions):
    fields = ['name']
