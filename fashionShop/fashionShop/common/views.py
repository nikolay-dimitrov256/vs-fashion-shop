from datetime import timedelta
from random import sample

from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, CreateView
from django.contrib import messages

from fashionShop import settings
from fashionShop.common.forms import ContactForm
from fashionShop.common.models import Feedback, ContactMessage
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
                    queryset=Picture.objects.all(),
                    to_attr='pictures_list'
                )
            )
            .filter(created_at__gt=now().date() - timedelta(days=90))
            .order_by('-created_at')[:10]
        )
        context['bestsellers'] = (
            Item.objects
            .exclude(deleted=True)
            .prefetch_related(
                Prefetch(
                    'pictures',
                    queryset=Picture.objects.all(),
                    to_attr='pictures_list'
                )
            )
            .filter(is_bestseller=True)[:10]
        )
        all_feedback = list(Feedback.objects.all())
        sample_size = min(len(all_feedback), 4) # Prevents error if looking for more elements than there are in the list
        feedback_sample = sample(all_feedback, sample_size)
        context['feedback'] = feedback_sample

        return context


class ContactView(TemplateView):
    template_name = 'common/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = ContactForm()

        return context


class ContactMessageView(CreateView):
    model = ContactMessage
    success_url = reverse_lazy('contact')
    form_class = ContactForm

    def form_invalid(self, form):
        return redirect('contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Thank you for your message, we will contact you as soon as possible.'))

        return HttpResponseRedirect(self.success_url)


class CategoryView(TemplateView):
    template_name = 'common/categories.html'


class SingleView(TemplateView):
    template_name = 'common/single.html'
