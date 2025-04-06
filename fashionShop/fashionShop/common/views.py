from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from fashionShop import settings


def set_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
        request.session['currency'] = currency

    next_page = request.POST.get('next', 'home')

    return redirect(next_page)


class HomeView(TemplateView):
    template_name = 'common/home.html'


class CategoryView(TemplateView):
    template_name = 'common/categories.html'


class SingleView(TemplateView):
    template_name = 'common/single.html'


class ContactView(TemplateView):
    template_name = 'common/contact.html'
