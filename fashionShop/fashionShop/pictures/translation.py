from modeltranslation.translator import register, TranslationOptions

from fashionShop.pictures.models import Picture


@register(Picture)
class PictureTranslationOptions(TranslationOptions):
    fields = ['description']
