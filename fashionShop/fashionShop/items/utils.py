import requests
from django.utils.text import slugify

from fashionShop.common.globals import BISOFT_API_URL
from fashionShop.common.utils import transliterate
from fashionShop.items.models import Item, Category, ColorGroup, Size, Stock
from fashionShop.stores.models import Store

BISOFT_COLOR_GROUPS = {
    1: 'white',
    2: 'beige',
    3: 'yellow',
    4: 'orange',
    5: 'red',
    6: 'bordeaux',
    7: 'pink',
    8: 'purple',
    9: 'sky blue',
    10: 'blue',
    11: 'green',
    12: 'dark green',
    13: 'brown',
    14: 'gray',
    15: 'black'
}


def check_and_create_color_groups():
    existing_color_groups = ColorGroup.objects.all()
    existing_color_group_names = [cg.name_en for cg in existing_color_groups]
    new_color_group_names = set(BISOFT_COLOR_GROUPS.values()) - set(existing_color_group_names)
    new_color_groups = [ColorGroup(name_en=name) for name in new_color_group_names]

    if len(new_color_groups) > 0:
        created_color_groups = ColorGroup.objects.bulk_create(new_color_groups)


def parse_and_save_items(data: list):
    for bisoft_item in data:
        item, created = Item.objects.get_or_create(item_number=bisoft_item['item_number'])
        item.name_bg = bisoft_item['name_bg']
        item.name_en = bisoft_item['name_en']
        item.description_bg = bisoft_item['description_bg']
        item.description_en = bisoft_item['description_en']
        #item.price = Decimal(bisoft_item['item_number__stores__price_2'])

        # if 0 < bisoft_item['item_number__stores__price_3'] < bisoft_item['item_number__stores__price_2']:
        #     item.discount_price = Decimal(bisoft_item['item_number__stores__price_3'])

        item.content_bg = bisoft_item['content_bg']
        item.content_eb = bisoft_item['content_en']

        category, created = Category.objects.get_or_create(name_en=bisoft_item['cat__key'])
        item.category = category

        if bisoft_item['color_group_en']:
            color_group, created = ColorGroup.objects.get_or_create(name_en=bisoft_item['color_group_en'])
            item.color_group = color_group

        item.save()

    for bisoft_item in data:
        item = Item.objects.filter(item_number=bisoft_item['item_number']).first()

        if not Item:
            continue

        bisoft_linked_items = [
            bisoft_item['add_1'], bisoft_item['add_2'], bisoft_item['add_3'],
            bisoft_item['add_4'], bisoft_item['add_5']
        ]

        for bisoft_linked_item in bisoft_linked_items:
            if bisoft_linked_item:
                linked_item = Item.objects.filter(item_number=bisoft_linked_item).first()
                if linked_item:
                    item.linked_items.add(linked_item)


def update_prices_and_stock():
    items = Item.objects.filter(deleted=False)

    response = requests.get(f'{BISOFT_API_URL}items/prices-stock/')
    data = response.json()

    for bisoft_item in data:
        item = items.filter(item_number=bisoft_item['item_number']).first()

        if not item:
            continue

        item.price = bisoft_item['stores__price_2']
        if 0 < bisoft_item['stores__price_3'] < bisoft_item['stores__price_2']:
            item.discount_price = bisoft_item['stores__price_3']

        for bisoft_size, quantity in bisoft_item['stock'].items():
            size, created = Size.objects.get_or_create(size=bisoft_size)

            stock, created = Stock.objects.get_or_create(item=item, size=size)

            stock.quantity = quantity
            stock.save()

        item.save()


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
    sizes_names_from_response = {s for sub in [it['sizes'].keys() for it in data] for s in sub}
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
            existing_item.slug = slugify(f"{item['item_number']}-{transliterate(item['name_bg'])}")
            existing_item.description_bg = item['description_bg'] if '=' not in item['description_bg'] else ''
            existing_item.description_en = item['description_en'] if '=' not in item['description_en'] else ''
            existing_item.price = item['price']
            existing_item.discount_price = item['sale_price']
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
                'price': item['price'],
                'discount_price': item['sale_price'],
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

    # Get Stocks to be created
    new_stocks = []

    for item in data:
        item['item_number'] = int(item['item_number'])
        stock_data = item['sizes']

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

        # Get and set linked items
        linked_items_from_request = [item['add_1'], item['add_2'], item['add_3'], item['add_4'], item['add_5']]
        linked_item_ids = {el for el in linked_items_from_request if el}

        if len(linked_item_ids) > 0:
            # linked_items = all_items.filter(item_number__in=linked_item_ids)
            linked_items = [items_map.get(item, None) for item in linked_item_ids if items_map.get(item, None)]
            item_to_link = items_map.get(item['item_number'])
            item_to_link.linked_items.set(linked_items)

    # Update existing stocks
    Stock.objects.bulk_update(list(existing_stocks), ['quantity'])
    # Create new stocks
    Stock.objects.bulk_create(new_stocks)
