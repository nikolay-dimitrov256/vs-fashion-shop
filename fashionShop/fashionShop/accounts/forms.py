from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from fashionShop.accounts.models import Profile

UserModel = get_user_model()


class AppUserCreateForm(BaseUserCreationForm):
    accepted_privacy_policy = forms.BooleanField(required=True,label=_("I agree to the Privacy Policy"),)
    accepted_marketing_emails = forms.BooleanField(required=False, label=_("I want to receive marketing emails"))

    class Meta:
        model = UserModel
        fields = ['email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get('accepted_privacy_policy'):
            raise ValidationError(_('You cannot register without agreeing to our Privacy Policy.'))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # user.set_password(self.cleaned_data["password"])

        if self.cleaned_data['accepted_privacy_policy']:
            user.accepted_privacy_policy = True
            user.accepted_privacy_policy_date = now()

        if self.cleaned_data['accepted_marketing_emails']:
            user.accepted_marketing_emails = True
            user.accepted_marketing_emails_date = now()

        if commit:
            user.save()
        return user


class AppUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
