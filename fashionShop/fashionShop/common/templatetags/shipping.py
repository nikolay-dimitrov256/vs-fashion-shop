from django import template

from fashionShop.common.globals import FREE_DELIVERY_THRESHOLD, CURRENCY_NAMES

register = template.Library()


@register.simple_tag
def free_shipping(request):
    # currency = request.session.get('currency', 'bgn')
    currency = 'bgn'

    return FREE_DELIVERY_THRESHOLD.get(currency.upper())


@register.simple_tag
def free_shipping_string(request):
    # currency = request.session.get('currency', 'bgn')
    currency = 'EUR'
    free_delivery_eur = FREE_DELIVERY_THRESHOLD.get('EUR')
    free_delivery_bgn = FREE_DELIVERY_THRESHOLD.get('BGN')
    currency_text_eur = CURRENCY_NAMES.get('EUR')
    currency_text_bgn = CURRENCY_NAMES.get('BGN')

    return f'{free_delivery_eur} {currency_text_eur} / {free_delivery_bgn} {currency_text_bgn}'


@register.filter
def is_free_shipping(total):
    return total > FREE_DELIVERY_THRESHOLD.get('EUR')
