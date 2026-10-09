import re
from decimal import Decimal
from pprint import pprint

import requests
import http.client
import json

from fashionShop.api.utils import get_econt_cities_data
from fashionShop.common.globals import SPEEDY_API_URL
from fashionShop.common.templatetags.shipping import is_free_shipping
from fashionShop.settings import INFOBIP_URL, INFOBIP_API_KEY, SPEEDY_USERNAME, SPEEDY_PASSWORD, ECONT_USERNAME, \
    ECONT_PASSWORD


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


def send_sms(to, message):
    payload = {
        'messages': [
            {
                'sender': 'Vili Stil',
                'destinations': [
                    {
                        'to': to
                    }
                ],
                'content': {
                    'text': message,
                    'transliteration': 'BULGARIAN_CYRILLIC',
                    'language': {
                        'languageCode': 'BG'
                    }
                }
            }
        ],
        'options': {
            'shortenUrl': True,
        }
    }

    headers = {
        'Authorization': f'App {INFOBIP_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(f'{INFOBIP_URL}/sms/3/messages', headers=headers, json=payload)

    print(response.json())


def find_speedy_office():
    site_id = '100'
    name = 'Стамболийски'

    url = f'{SPEEDY_API_URL}/location/site'
    headers = {
        'Content-Type': 'application/json',
        'charset': 'utf-8',
    }
    params = {
        'userName': SPEEDY_USERNAME,
        'password': SPEEDY_PASSWORD,
        'language': 'BG',
        'countryId': '100',  # Bulgaria
        # 'siteId': site_id,
        'name': name,
    }

    response = requests.post(
        url=url,
        headers=headers,
        json=params,
    )

    data = response.json()

    pprint(data)


def find_econt_town():
    query = 'Stamboliyski'
    data = get_econt_cities_data()

    cities = [
        {
            'id': city['id'],
            'postCode': city['postCode'],
            'name': city['name'],
            'regionName': city['regionName'],
            # 'servingOffices': {of["officeCode"] for of in city['servingOffices']},
        }
        for city in data['cities']
        if city.get('name', '').lower().startswith(query.lower())
           or city.get('nameEn', '').lower().startswith(query.lower())
    ]

    pprint(cities)
