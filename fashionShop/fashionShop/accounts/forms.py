from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm, UserChangeForm
from django import forms

from fashionShop.accounts.models import Profile

UserModel = get_user_model()


class AppUserCreateForm(BaseUserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email']


class AppUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
