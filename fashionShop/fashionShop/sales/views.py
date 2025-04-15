from copy import deepcopy

from django.contrib import messages
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
            cart = request.session.get('cart', {})
            if item.item_number not in cart.keys():
                cart[item.item_number] = {size: quantity}
            else:
                if size not in cart[item.item_number]:
                    cart[item.item_number] = {size: quantity}
                else:
                    cart[item.item_number][size] += quantity

            request.session['cart'] = cart

        messages.success(request,f"{item.name} {_('was successfully added to cart.')}")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


def view_cart_view(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_cart = request.session.get('cart', {})
        cart = deepcopy(session_cart)

        for item_number, data in cart.items():
            item = Item.objects.filter(pk=item_number).first()

            if not item:  # fail silently
                continue

            cart[item_number]['item'] = item

    context = {
        'cart': cart
    }

    return render(request, 'sales/cart.html', context)