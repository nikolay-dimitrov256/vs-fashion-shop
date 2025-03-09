from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from fashionShop.accounts.forms import AppUserCreateForm

UserModel = get_user_model()


def test(request):
    return render(request, 'accounts/test.html')


def login(request):
    return render(request, 'accounts/login.html')


class AppUserRegisterView(CreateView):
    model = UserModel
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    form_class = AppUserCreateForm

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)


class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)
