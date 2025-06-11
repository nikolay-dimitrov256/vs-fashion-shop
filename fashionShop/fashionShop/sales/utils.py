from fashionShop.items.models import OrderItem, Size, Item, CartItem
from fashionShop.sales.models import Cart


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
                at_price=cart_item.item.final_price
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
                )
                order_items.append(order_item)

        request.session['cart'] = {}

    return OrderItem.objects.bulk_create(order_items)


def refresh_orders(modeladmin, request, queryset):
    for order in queryset:
        for item in order.order_items.all():
            item.save()

        order.save()


refresh_orders.short_description = 'Refresh orders'
