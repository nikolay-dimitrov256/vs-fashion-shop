from django import forms
from django.utils.translation import gettext_lazy as _

from fashionShop.reviews.models import Review


class ReviewCreateForm(forms.ModelForm):
    author = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Your name*')}),
        label=''
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Title')}),
        required=False,
        label=''
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': _('Your review*')}),
        label=''
    )

    class Meta:
        model = Review
        fields = ['author', 'title', 'content', 'rating']
        widgets = {
            'rating': forms.HiddenInput()
        }
