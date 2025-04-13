from django.db import models
from django.utils.translation import gettext_lazy as _

from fashionShop.items.models.item import Item
from fashionShop.items.models.size import Size


class Stock(models.Model):
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
    )

    store = models.ForeignKey(
        to='stores.Store',
        on_delete=models.CASCADE,
    )

    size = models.ForeignKey(
        to=Size,
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField(
        default=0
    )

    class Meta:
        unique_together = [['item', 'store', 'size']]
        verbose_name = _('stock')
        verbose_name_plural = _('stock')

    def __str__(self):
        return f'{str(self.item)} - {self.size.size}'
