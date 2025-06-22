from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _

from fashionShop.common.utils import get_client_ip
from fashionShop.items.models import Item
from fashionShop.reviews.forms import ReviewCreateForm
from fashionShop.reviews.models import Review


def submit_review(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if request.method == 'POST':
        ip = get_client_ip(request)

        # Check if this IP already submitted a review for this item
        if Review.objects.filter(item=item, ip_address=ip).exists():
            messages.error(request, _('You have already sent a review for this product.'))
            return redirect('item-details', slug=item.slug)

        form = ReviewCreateForm(request.POST or None)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.ip_address = ip
            review.save()
            messages.success(request, _('Your review was submitted successfully.'))
            return redirect('item-details', slug=item.slug)

    # fallback: redisplay the item with errors
    return redirect('item-details', slug=item.slug)
