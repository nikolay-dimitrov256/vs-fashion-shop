from django.contrib.auth import user_logged_in, get_user_model
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from fashionShop.items.models import Item, Size, CartItem, OrderRefundItem
from fashionShop.sales.models import Cart, OnlineOrder, OnlineRefund


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


@receiver(post_save, sender=OnlineRefund)
def calculate_refund(sender, instance, created, **kwargs):
    if created:
        if instance.refund_all:
            refund_items = []
            for item in instance.order.order_items.all():
                refund_item = OrderRefundItem(
                    order_item = item,
                    refund = instance,
                    quantity = item.quantity,
                    total_price = item.total_price,
                )

                refund_items.append(refund_item)

            OrderRefundItem.objects.bulk_create(refund_items)

    instance.refresh_from_db()
    total = sum(item.total_price for item in instance.items.all())

    if total != instance.total:
        OnlineRefund.objects.filter(pk=instance.pk).update(total=total)


@receiver(post_delete, sender=OrderRefundItem)
def calculate_refund_after_item_delete(sender, instance, **kwargs):
    refund = instance.refund

    total = sum(item.total_price for item in refund.items.all())

    if total != refund.total:
        OnlineRefund.objects.filter(pk=refund.pk).update(total=total)