from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import TemplateView

from fashionShop.items.models import Size


class SalesBySizeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/sales-by-size.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['sizes'] = Size.objects.annotate(sales=Sum('order_items__quantity')).order_by('size')

        return context

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
