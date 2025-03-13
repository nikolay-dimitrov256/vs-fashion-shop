from fashionShop.items.models import Item, Category, ColorGroup


def parse_and_save_items(data: list):
    for bisoft_item in data:
        item, created = Item.objects.get_or_create(item_number=bisoft_item['item_number'])
        item.name_bg = bisoft_item['name_bg']
        item.name_en = bisoft_item['name_en']
        item.description_bg = bisoft_item['description_bg']
        item.description_en = bisoft_item['description_en']
        item.price = bisoft_item['item_number__stores__price_2']

        if 0 < bisoft_item['item_number__stores__price_3'] < item.price:
            item.discount_price = bisoft_item['item_number__stores__price_3']

        item.content_bg = bisoft_item['content_bg']
        item.content_eb = bisoft_item['content_en']

        category, created = Category.objects.get_or_create(name_en=bisoft_item['cat__key'])
        item.category = category

        if bisoft_item['color_group_en']:
            color_group, created = ColorGroup.objects.get_or_create(name_en=bisoft_item['color_group_en'])
            item.color_group = color_group

        bisoft_linked_items = [
            bisoft_item['add_1'], bisoft_item['add_2'], bisoft_item['add_3'],
            bisoft_item['add_4'], bisoft_item['add_5']
        ]

        for bisoft_linked_item in bisoft_linked_items:
            if bisoft_linked_item:
                linked_item, created = Item.objects.get_or_create(item_number=bisoft_linked_item)
                item.linked_items.add(linked_item)

        item.save()
