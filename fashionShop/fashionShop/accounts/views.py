from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView

from fashionShop.accounts.forms import AppUserCreateForm

UserModel = get_user_model()


def test(request):
    return render(request, 'accounts/test.html')


class AppUserRegisterView(CreateView):
    model = UserModel
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    form_class = AppUserCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if self.object.accepted_privacy_policy:
            self.object.accepted_privacy_policy_date = now()

        if self.object.accepted_marketing_emails:
            self.object.accepted_marketing_emails_date = now()

        self.object.save()

        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')

        return HttpResponseRedirect(self.get_success_url())

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
