import requests
from celery import shared_task

from fashionShop.common.templatetags.shipping import is_free_shipping
from fashionShop.sales.choices import ShippingChoices
from fashionShop.sales.models import OnlineOrder
from fashionShop.settings import INFOBIP_API_KEY, INFOBIP_URL


@shared_task
def send_bisoft_report(order_id, save=True):
    order = OnlineOrder.objects.get(pk=order_id)

    report = {'user': {}, 'basket': {}}

    report['user']['name'] = order.full_name or 'анонимен'
    report['user']['doc_num'] = order.order_code if order.order_code else 0
    report['user']['total'] = str(order.total)
    report['user']['date'] = str(order.created_at.date())
    report['user']['delivery'] = 0 if is_free_shipping(order.total) else 5.99
    report['user']['phone'] = order.phone

    if ShippingChoices.is_address(order.shipping_method):
        report['user']['address'] = str(order.address)
    elif ShippingChoices.is_office(order.shipping_method):
        report['user']['address'] = order.get_shipping_method_display()
    else:
        report['user']['address'] = 'няма информация за адрес'

    total_quantity = 0

    for order_item in order.order_items.all():
        item_number = str(order_item.item.pk)
        size = order_item.size.size
        total_quantity += order_item.quantity

        if item_number not in report['basket']:
            report['basket'][item_number] = {}
            report['basket'][item_number]['sizes'] = {}
        report['basket'][item_number]['sizes'][size] = order_item.quantity
        report['basket'][item_number]['price'] = str(order_item.at_price)

    report['user']['total_quantity'] = total_quantity

    # url = f'https://vilistil.com/get_sale.php?order={order.order_code}&lic=license'
    url = f'https://vilistil.com/order/{order.order_code}/licence'
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        print('Sending report for:', order.order_code)
        print('Payload:', report)
        response = requests.post(url, json=report, headers=headers)
        print('Status:', response.status_code)
        print('Response:', response.text)
        data = response.json()

        if data['success']:
            if save:
                order.bisoft_report_sent = True
                order.save()

        return data['success']

    except Exception as e:
        print(str(e))
        return False


@shared_task
def send_sms(to: str, message: str | None) -> dict | None:
    return None
    if not to or not message:
        return None

    payload = {
        'messages': [
            {
                'sender': 'InfoSMS',
                'destinations': [
                    {
                        'to': to
                    }
                ],
                'content': {
                    'text': message,
                    # 'transliteration': 'BULGARIAN_CYRILLIC',
                    'language': {
                        'languageCode': 'BG'
                    }
                }
            }
        ],
        'urlOptions': {
            'shortenUrl': True,
        },
        'includeSmsCountInResponse': True,
    }

    headers = {
        'Authorization': f'App {INFOBIP_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        response = requests.post(f'{INFOBIP_URL}/sms/3/messages', headers=headers, json=payload)

        return response.json()

    except Exception:
        return None
