from decimal import Decimal, ROUND_HALF_UP

import requests
from celery import shared_task
from django.utils.text import slugify

from fashionShop.common.globals import BISOFT_API_URL, EURO_RATE
from fashionShop.common.utils import transliterate
from fashionShop.items.models import ColorGroup, Category, Size, Item, Stock
from fashionShop.items.utils import check_and_create_color_groups, BISOFT_COLOR_GROUPS
from fashionShop.stores.models import Store


@shared_task
def add(x, y):
    return x + y


@shared_task
def load_items_from_bisoft():
    # Fetch data from API
    url = f'{BISOFT_API_URL}cat/all'
    response = requests.get(url)
    data = response.json()

    # Get store
    store = Store.objects.filter(id=0).first()
    if store is None:
        return None

    # Load color groups
    check_and_create_color_groups()
    all_color_groups = ColorGroup.objects.all()
    color_group_map = {cg.name_en: cg for cg in all_color_groups}

    # Get and create categories
    existing_categories = Category.objects.all()
    existing_categories_names = {c.name_en for c in existing_categories}
    category_names_from_response = {it['category'] for it in data}
    new_categories_names = category_names_from_response -  existing_categories_names
    new_categories = [Category(name_en=name) for name in new_categories_names]
    Category.objects.bulk_create(new_categories)
    all_categories = Category.objects.all()
    category_map = {c.name_en: c for c in all_categories}

    # Get and create sizes
    existing_sizes = Size.objects.all()
    existing_sizes_names = {s.size for s in existing_sizes}
    # sizes_names_from_response = {s for sub in [it['sizes'].keys() for it in data] for s in sub}
    sizes_names_from_response = {
        size
        for item in data
        if isinstance(item['sizes'], dict)
        for size in item['sizes']
    }
    new_sizes_names = sizes_names_from_response - existing_sizes_names
    new_sizes = [Size(size=s) for s in new_sizes_names]
    Size.objects.bulk_create(new_sizes)
    all_sizes = Size.objects.all()
    sizes_map = {s.size: s for s in all_sizes}

    # Get all items to be modified
    existing_items_list = list(Item.objects.all())
    # existing_items_ids = {it.item_number for it in existing_items_list}
    existing_items_map = {it.item_number: it for it in existing_items_list}

    # Get all items to be created
    new_items_list = []

    # Get created items and data for existing items update
    for item in data:
        item['item_number'] = int(item['item_number'])
        group_color_id = item.get('group_color', 0)
        color_group_name = BISOFT_COLOR_GROUPS.get(group_color_id, '')
        color_group = color_group_map.get(color_group_name, None)
        category = category_map.get(item['category'], None)

        if item['item_number'] in existing_items_map:  # The item exists
            # existing_item = next((it for it in existing_items_list if it.item_number == item['item_number']), None)
            existing_item = existing_items_map.get(item['item_number'])
            existing_item.name_bg = item['name_bg']
            existing_item.name_en = item['name_en']
            # existing_item.slug = slugify(f"{item['item_number']}-{transliterate(item['name_bg'])}")
            existing_item.description_bg = item['description_bg'] if '=' not in item['description_bg'] else ''
            existing_item.description_en = item['description_en'] if '=' not in item['description_en'] else ''
            existing_item.price = Decimal(item['price'])
            existing_item.discount_price = Decimal(item['sale_price'])
            existing_item.content_bg = item['content_bg']
            existing_item.content_en = item['content_en']

            existing_item.category = category
            existing_item.color_group = color_group

        else:  # The item is new
            item_data = {
                'item_number': item['item_number'],
                'name_bg': item['name_bg'],
                'name_en': item['name_en'],
                'slug': slugify(f"{item['item_number']}-{transliterate(item['name_bg'])}"),
                'description_bg': item['description_bg'] if '=' not in item['description_bg'] else '',
                'description_en': item['description_en'] if '=' not in item['description_en'] else '',
                'price': Decimal(item['price']),
                'discount_price': Decimal(item['sale_price']),
                'content_bg': item['content_bg'],
                'content_en': item['content_en'],
            }
            new_item = Item(**item_data)
            new_item.category = category
            new_item.color_group = color_group

            new_items_list.append(new_item)

    # Modify existing items
    Item.objects.bulk_update(
        existing_items_list,
        ['name_bg', 'name_en', 'slug', 'description_bg', 'description_en', 'price', 'discount_price',
         'content_bg', 'content_en', 'color_group', 'category']
    )

    # Create new items
    Item.objects.bulk_create(new_items_list)

    all_items = Item.objects.all()
    items_map = {it.item_number: it for it in all_items}

    # Get Stocks to be updated
    existing_stocks = Stock.objects.filter(store__id=0)
    stocks_to_nullify = []

    # Get Stocks to be created
    new_stocks = []

    for item in data:
        item['item_number'] = int(item['item_number'])
        stock_data = item['sizes'] if isinstance(item['sizes'], dict) else {}
        existing_item_stocks = existing_stocks.filter(item__item_number=item['item_number'])

        # Get and set stocks
        for size, quantity in stock_data.items():
            existing_stock = existing_stocks.filter(item__item_number=item['item_number'], size__size=size).first()

            if existing_stock:
                existing_stock.quantity = quantity
            else:
                item_obj = items_map.get(item['item_number'])
                size_obj = sizes_map.get(size)
                new_stock = Stock(item=item_obj, store=store, size=size_obj, quantity=quantity)
                new_stocks.append(new_stock)

        for stock in existing_item_stocks:
            if stock.size.size not in stock_data:
                stock.quantity = 0
                stocks_to_nullify.append(stock)

        # Get and set linked items
        linked_items_from_request = [item['add_1'], item['add_2'], item['add_3'], item['add_4'], item['add_5']]
        linked_item_ids = {el for el in linked_items_from_request if el}

        if len(linked_item_ids) > 0:
            # linked_items = all_items.filter(item_number__in=linked_item_ids)
            linked_items = [items_map.get(item, None) for item in linked_item_ids if items_map.get(item, None)]
            item_to_link = items_map.get(item['item_number'])
            item_to_link.linked_items.add(*linked_items)

    # Update existing stocks
    Stock.objects.bulk_update(list(existing_stocks), ['quantity'])
    Stock.objects.bulk_update(stocks_to_nullify, ['quantity'])
    # Create new stocks
    Stock.objects.bulk_create(new_stocks)


@shared_task
def check_sizes():
    url = f'{BISOFT_API_URL}cat/all'
    response = requests.get(url)
    data = response.json()

    sizes_names_from_response = {
        size
        for item in data
        if isinstance(item['sizes'], dict)
        for size in item['sizes']
    }

    print(sizes_names_from_response)
