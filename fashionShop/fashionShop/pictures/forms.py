from django import forms

from fashionShop.pictures.models import ReviewPicture
from fashionShop.reviews.models import Review

ReviewPictureFormSet = forms.inlineformset_factory(
    Review,
    ReviewPicture,
    fields=('image',),
    extra=3,
    max_num=5
)