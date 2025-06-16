from django import forms
from django.utils.translation import gettext_lazy as _

from fashionShop.common.models import ContactMessage, Address


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'id': 'input_name',
                'name': 'name',
                'class': 'form_input input_name input_ph',
                'placeholder': _('Name'),
                'data-error': _('Name is required.'),
            }
        ),
    )

    email = forms.EmailField(
        label='',
        required=False,
        widget=forms.EmailInput(
            attrs={
                'id': 'input_email',
                'name': 'email',
                'class': 'form_input input_email input_ph',
                'placeholder': _('Email'),
            }
        )
    )

    phone = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                'name': 'phone',
                'class': 'form_input input_ph',
                'placeholder': _('Phone'),
            }
        )
    )

    message = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'name': 'message',
                'class': 'input_ph input_message',
                'placeholder': _('Message'),
                'data-error': _('Please, write something to us.')
            }
        )
    )
    class Meta:
        model = ContactMessage
        fields = '__all__'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['store', 'user']


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('Search')}),
    )
