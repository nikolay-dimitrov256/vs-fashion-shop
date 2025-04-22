from django import forms

from fashionShop.sales.models import OnlineOrder


class PhoneOrderForm(forms.ModelForm):
    class Meta:
        model = OnlineOrder
        fields = ['phone']
