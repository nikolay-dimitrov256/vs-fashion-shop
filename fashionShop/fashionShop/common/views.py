from datetime import timedelta

from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from fashionShop import settings
from fashionShop.items.models import Item
from fashionShop.pictures.models import Picture


def set_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
        request.session['currency'] = currency

    next_page = request.POST.get('next', 'home')

    return redirect(next_page)


class HomeView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['new_arrivals'] = (
            Item.objects
            .exclude(deleted=True)
            .prefetch_related(
                Prefetch(
                    'pictures',
                    queryset=Picture.objects.all(),  # Only fetch the first image
                    to_attr='pictures_list'
                )
            )
            .filter(created_at__gt=now().date() - timedelta(days=90))
            .order_by('-created_at')[:10]
        )
        context['bestsellers'] = (
            Item.objects
            .prefetch_related(
                Prefetch(
                    'pictures',
                    queryset=Picture.objects.all()[:1],  # Only fetch the first image
                    to_attr='main_picture_list'
                )
            )
            .filter(is_bestseller=True)
        )

        return context


class CategoryView(TemplateView):
    template_name = 'common/categories.html'


class SingleView(TemplateView):
    template_name = 'common/single.html'


class ContactView(TemplateView):
    template_name = 'common/contact.html'
