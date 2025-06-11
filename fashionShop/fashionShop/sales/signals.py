from django.contrib.auth import user_logged_in, get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from fashionShop.items.models import Item, Size, CartItem
from fashionShop.sales.models import Cart, OnlineOrder


# UserModel = get_user_model()


@receiver(user_logged_in)
def sync_session_cart(sender, user, request, **kwargs):
    session_cart = request.session.get('cart', {})
    if not session_cart:
        return

    cart, created = Cart.objects.get_or_create(user=user)

    for item_number, data in session_cart.items():
        item = Item.objects.filter(pk=item_number).first()
        if not item:  # fail silently
            continue

        for size, quantity in data.items():
            try:
                size_obj = Size.objects.get(size=size)
                quantity = int(quantity)
            except:  # fail silently
                continue

            cart_item, created = CartItem.objects.get_or_create(item=item, cart=cart, size=size_obj)

            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity

            cart_item.save()
            cart.save()

    request.session['cart'] = {}


@receiver(post_save, sender=OnlineOrder)
def calculate_total(sender, instance, **kwargs):
    total = sum(item.total_price for item in instance.order_items.all())

    if total != instance.total:
        OnlineOrder.objects.filter(pk=instance.pk).update(total=total)
