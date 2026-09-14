from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from fashionShop.items.models import OrderItem
from fashionShop.sales.utils import update_order_total


@receiver(post_save, sender=OrderItem)
def calculate_order_total(sender, instance, created, **kwargs):
    if created:
        return

    update_order_total(instance.order)
