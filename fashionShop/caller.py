from decimal import Decimal
from pprint import pprint

import requests
import http.client
import json

from fashionShop.common.templatetags.shipping import is_free_shipping
from fashionShop.settings import INFOBIP_URL, INFOBIP_API_KEY

recepient = "359886531811"


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


def send_sms_http():
    BASE_URL = INFOBIP_URL
    conn = http.client.HTTPSConnection(BASE_URL)
    payload = json.dumps({
        "messages": [
            {
                "sender": "InfoSMS",
                "destinations": [
                    {
                        "to": "41793026727"
                    }
                ],
                "content": {
                    "text": "This is a sample message"
                }
            }
        ]
    })
    headers = {
        'Authorization': '{authorization}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn.request("POST", "/sms/3/messages", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


def send_sms():
    payload = {
        "messages": [
            {
                "sender": "InfoSMS",
                "destinations": [
                    {
                        "to": recepient
                    }
                ],
                "content": {
                    "text": "This is a sample message"
                }
            }
        ]
    }
    headers = {
        'Authorization': f'App {INFOBIP_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(f'{INFOBIP_URL}/sms/3/messages', headers=headers, json=payload)

    print(response.json())


send_sms()
