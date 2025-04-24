from django import forms

from fashionShop.sales.choices import ShippingChoices
from fashionShop.sales.models import OnlineOrder


class PhoneOrderForm(forms.ModelForm):
    class Meta:
        model = OnlineOrder
        fields = ['phone']


class ShippingOrderForm(forms.ModelForm):
    office = forms.CharField(
        widget=forms.Select(),
        required=False,
    )
    def __init__(self, *args, **kwargs):
        self.address_form = kwargs.pop('address_form', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = OnlineOrder
        exclude = ['user', 'created_at', 'updated_at', 'address']

    def is_valid(self) -> bool:
        valid = super().is_valid()
        address_valid = self.address_form.is_valid() if self.address_form else True

        return valid and address_valid

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('shipping_method')

        if not method:
            self.add_error('shipping_method', 'Please select a shipping method.')
            return cleaned_data  # Early return to avoid more logic without a method

        if ShippingChoices.is_office(method):
            if not cleaned_data.get('town') or not cleaned_data.get('office'):
                self.add_error(None, 'Please provide both town and office for office delivery.')
            cleaned_data['address'] = None

        elif ShippingChoices.is_address(method):
            cleaned_data['town'] = None
            cleaned_data['office'] = None

        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)

        if ShippingChoices.is_address(self.cleaned_data.get('shipping_method')):
            address = self.address_form.save()
            order.address = address
        else:
            order.address = None

        if commit:
            order.save()

        return order
