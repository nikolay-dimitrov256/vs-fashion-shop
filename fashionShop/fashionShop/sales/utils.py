from fashionShop.items.models import OrderItem, Size, Item, CartItem, Stock
from fashionShop.sales.models import Cart

BISOFT_SIZE_RANGES_MAP = {
    '40': {'40': 1, '42': 2, '44': 3, '46': 4, '48': 5, '50': 6, '52': 7, '54': 8, '56': 9, '58': 0},
    'c46': {'46': 1, '48': 2, '50': 3, '52': 4, '54': 5, '56': 6, '58': 7, '60': 8, '62': 9, '64': 0},
    '48': {'50': 1, '52': 2, '54': 3, '56': 4, '58': 5, '60': 6, '62': 7, '64': 8, '66': 9, '48': 0},
    '50': {'50': 1, '52': 2, '54': 3, '56': 4, '58': 5, '60': 6, '62': 7, '64': 8, '66': 9, '68': 0},
    's': {'S': 1, 'M': 2, 'L': 3, 'XL': 4, '2XL': 5, '3XL': 6, '4XL': 7, '5XL': 8, '6XL': 9, '7XL': 0},
    'xs': {'S': 1, 'M': 2, 'L': 3, 'XL': 4, '2XL': 5, '3XL': 6, '4XL': 7, '5XL': 8, '6XL': 9, 'XS': 0},
    '-1': {'40': 1, '42': 2, '44': 3, '46': 4, '48': 5, '50': 6, '52': 7, '54': 8, '56': 9, '58': 0},
}


def fill_order_from_cart_empty_cart(request, order):
    order_items = []

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

        for cart_item in cart.cart_items.all():
            order_item = OrderItem(
                item=cart_item.item,
                order=order,
                size=cart_item.size,
                quantity=cart_item.quantity,
                at_price=cart_item.item.final_price,
                total_price=cart_item.quantity * cart_item.item.final_price,
            )
            order_items.append(order_item)

        CartItem.objects.filter(cart=cart).delete()  # Empty the cart
    else:
        cart = request.session.get('cart', {})

        for item_number, sizes in cart.items():
            item = Item.objects.filter(item_number=item_number).first()
            for size, quantity in sizes.items():
                size_obj = Size.objects.filter(size=size).first()
                order_item = OrderItem(
                    item=item,
                    order=order,
                    size=size_obj,
                    quantity=int(quantity),
                    at_price=item.final_price,
                    total_price=int(quantity) * item.final_price,
                )
                order_items.append(order_item)

        request.session['cart'] = {}

    return OrderItem.objects.bulk_create(order_items)


def get_bisoft_column(size: Size, item: Item) -> int:
    # get starting size
    starting_size = item.starting_size

    # get size range
    size_range = BISOFT_SIZE_RANGES_MAP.get(starting_size, BISOFT_SIZE_RANGES_MAP['40'])

    # check if size is translated
    stock = Stock.objects.filter(item=item, translated_size=size, translated_size__isnull=False).first()
    actual_size = size.size
    if stock is not None:
        actual_size = stock.size.size

    # get bisoft column
    bisoft_column = size_range.get(actual_size, 1)

    return bisoft_column
