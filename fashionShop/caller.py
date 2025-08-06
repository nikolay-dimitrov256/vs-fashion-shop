from decimal import Decimal
from pprint import pprint

import requests

from fashionShop.common.templatetags.shipping import is_free_shipping


def send_bisoft_request():
    payload = {'basket': {'10329': {'price': '65.00', 'sizes': {'42': 1}}},
 'user': {'address': 'няма информация за адрес',
          'date': '2025-08-06',
          'delivery': 5.99,
          'doc_num': '2508490058',
          'name': 'анонимен',
          'phone': '0886531811',
          'total': '65.00',
          'total_quantity': 1}}


    url = f'https://vilistil.com/get_sale.php?order=2508490058&lic=license'

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    print(response.json())


send_bisoft_request()
