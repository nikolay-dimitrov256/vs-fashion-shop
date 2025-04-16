from _decimal import Decimal
from copy import deepcopy

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic import DetailView

from fashionShop.items.models import CartItem, Item, Size
from fashionShop.sales.models import Cart


def add_to_cart(request, pk):
    if request.method == 'POST':
        # Get the item
        item = Item.objects.filter(pk=pk).first()
        # Validate the item exists
        if not item:
            messages.error(request, _('The item was not found.'))
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        size = request.POST.get('size')
        quantity = request.POST.get('quantity')
        # Validate the size and quantity are correct
        try:
            size_obj = Size.objects.get(size=size)
            quantity = int(quantity)
        except Exception:
            messages.error(request, _('There was a problem with your request.'))
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item, size=size_obj)

            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity

            cart.save()
            cart_item.save()

        else:
            item_number = str(pk)
            cart = request.session.get('cart', {})
            print(cart)
            if item_number not in cart.keys():
                cart[item_number] = {size: quantity}
            else:
                if size not in cart[item_number]:
                    cart[item_number][size] = quantity
                else:
                    cart[item_number][size] += quantity
            print(cart)
            request.session['cart'] = cart

        message_text = _('was successfully added to cart.')
        messages.success(request, f"{item.name} {message_text}")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


def view_cart_view(request):
    if request.user.is_authenticated:
        cart = (
            Cart.objects
            .prefetch_related(
                'cart_items__item__pictures',
                'cart_items__size'
            )
            .filter(user=request.user)
            .first()
        )
        if cart:
            cart.total = sum(i.total_price for i in cart.cart_items.all())

        context = {
            'cart': cart,
        }

    else:
        session_cart = request.session.get('cart', {})
        cart = deepcopy(session_cart)
        cart_total = Decimal(0)
        items = Item.objects.filter(item_number__in=cart.keys())
        items_map = {item.item_number: item for item in items}

        for item_number, data in cart.items():
            item = items_map.get(int(item_number))
            cart[item_number] = {'sizes': data, 'item': item}
            total = sum(item.final_price * int(q) for s, q in data.items())
            cart[item_number]['total'] = total
            cart_total += total

        context = {
            'cart': cart,
            'cart_total': cart_total
        }

    return render(request, 'sales/cart.html', context)


def remove_from_cart(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            if not cart:
                message = _('Your cart is empty.')
                messages.info(request, message)
                return redirect('view-cart')

            size = request.POST.get('size')
            size_obj = Size.objects.filter(size=size).first()
            item = Item.objects.filter(pk=pk).first()
            cart_item = CartItem.objects.filter(cart=cart, item=item, size=size_obj).first()

            if cart_item:
                cart_item.delete()

            message = _('was removed successfully.')
            messages.info(request, f'{item.name} {message}')

        else:
            cart = request.session.get('cart', {})

            if not cart:
                message = _('Your cart is empty.')
                messages.info(request, message)
                return redirect('view-cart')

            size = request.POST.get('size')
            item = Item.objects.filter(pk=pk).first()
            pk = str(pk)

            if pk in cart.keys():
                if size in cart[pk].keys():
                    del cart[pk][size]
                    if not cart[pk]:
                        del cart[pk]

            request.session['cart'] = cart
            message = _('was removed successfully.')
            messages.info(request, f'{item.name} {message}')

    return redirect('view-cart')
