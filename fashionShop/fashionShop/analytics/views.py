from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Q, F, Case, When, Value, FloatField, DecimalField
from django.db.models.functions import Coalesce, Cast
from django.shortcuts import render
from django.views.generic import TemplateView

from fashionShop.items.models import Size
from fashionShop.sales.choices import StatusChoices


class SalesBySizeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/sales-by-size.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['sizes'] = Size.objects.annotate(sales=Sum('order_items__quantity')).order_by('size')

        return context

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class OrderStatusBySizeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/order-status-by-size.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sizes'] = (Size.objects
        .annotate(
            total_orders=Coalesce(Sum('order_items__quantity'), 0),
            successful=Coalesce(
                Sum('order_items__quantity', filter=Q(order_items__order__status__in=[
                StatusChoices.COMPLETED, StatusChoices.REPLACED])),
            0),
            failed=Coalesce(
                Sum('order_items__quantity', filter=Q(order_items__order__status__in=[
                StatusChoices.REFUNDED, StatusChoices.ABANDONED, StatusChoices.REJECTED, StatusChoices.CANCELED
            ])),
            0),
            not_completed=Coalesce(
                Sum('order_items__quantity', filter=Q(order_items__order__status__in=[
                StatusChoices.PENDING, StatusChoices.SENT, StatusChoices.CONFIRMED
            ])),
            0),
            revenue=Coalesce(
                Sum(
                    F('order_items__at_price') * F('order_items__quantity'),
                    filter=Q(order_items__order__status__in=[
                        StatusChoices.COMPLETED, StatusChoices.REPLACED
                    ]),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                ),
                Value(0, output_field=DecimalField(max_digits=10, decimal_places=2))
            )
        )
        .annotate(
            percent_successful=Case(
                When(total_orders=0, then=Value(0.0)),
                default=Cast(F('successful'), FloatField()) / Cast(F('total_orders'), FloatField()) * 100.0,
                output_field=FloatField()
            ),
            percent_failed=Case(
                When(total_orders=0, then=Value(0.0)),
                default=Cast(F('failed'), FloatField()) / Cast(F('total_orders'), FloatField()) * 100.0,
                output_field=FloatField()
            ),
        )
        .order_by('size')
        )

        return context

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
