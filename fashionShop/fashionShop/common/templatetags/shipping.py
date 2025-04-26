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
    currency = 'bgn'
    free_delivery = FREE_DELIVERY_THRESHOLD.get(currency.upper())
    currency_text = CURRENCY_NAMES.get(currency.upper())

    return f'{free_delivery}{currency_text}'


@register.filter
def is_free_shipping(total):
    return total <= FREE_DELIVERY_THRESHOLD.get('BGN')
