from pprint import pprint

import requests
import time

from fashionShop.common.globals import BISOFT_API_URL, SPEEDY_API_URL


def send_request():
    start = time.time()

    url = 'https://vilistil.com/vs/item/10015'
    #url = 'https://vilistil.com/vs/cat/all'
    #url = 'http://127.0.0.1:8001/items/prices-stock/'
    #url = 'https://api.exchangerate-api.com/v4/latest/GBP'
    #url = 'https://vilistil.com/bisoft/xauge.php/feeds/vshop?c1=cat&c2=pants'
    #url = 'https://vilistil.com/bisoft/xauge.php/feeds/vshop?c1=item&c2=50412'
    #url = 'https://bisoft.style.bg/item.php'
    #url = 'https://vilistil.com/vshop.php?c1=item&c2=50412'

    response = requests.get(url)

    end = time.time()

    data = response.json()
    #item_numbers = [el['item_number'] for el in data]
    pprint(data)
    print(len(data))
    print(f'The request took {end - start} seconds')


def test_flattening():
    url = f'{BISOFT_API_URL}cat/all'
    response = requests.get(url)
    data = response.json()

    new_sizes_names = {s for sub in [it['sizes'].keys() for it in data] for s in sub}

    print(new_sizes_names)


def find_town_request():
    base_url = 'https://api.speedy.bg/v1'
    url = f'{base_url}/location/site'
    headers = {
        'Content-Type': 'application/json',
        'charset': 'utf-8',

    }
    params = {
        'userName': '1996022',
        'password': '1243131659',
        'language': 'BG',
        'countryId': '100',  # Bulgaria
        'name': 'Стамболийски',
    }

    response = requests.post(
        url=url,
        headers=headers,
        json=params,
    )

    pprint(response.json())


def find_office():
    query = '51980'

    url = f'{SPEEDY_API_URL}/location/office'
    headers = {
        'Content-Type': 'application/json',
        'charset': 'utf-8',

    }
    params = {
        'userName': '1996022',
        'password': '1243131659',
        'language': 'BG',
        'countryId': '100',  # Bulgaria
        'siteId': query,
    }

    response = requests.post(
        url=url,
        headers=headers,
        json=params,
    )

    data = response.json()

    for office in data['offices']:
        pprint(office)


print(len('201 - СТАМБОЛИЙСКИ - ул. ХРИСТО БОТЕВ No 7'))