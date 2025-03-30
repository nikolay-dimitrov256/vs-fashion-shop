from cloudinary.models import CloudinaryField
from django.db import models

from fashionShop.items.models import Item


class Picture(models.Model):
    image = CloudinaryField('image')

    is_main = models.BooleanField(
        default=False,
    )

    is_detail = models.BooleanField(
        default=False,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        related_name='pictures'
    )

    class Meta:
        ordering = ['-is_main', 'is_detail', '-created_at']

    def save(self, *args, **kwargs):
        if self.is_main:
            Picture.objects.filter(item=self.item, is_main=True).exclude(id=self.id).update(is_main=False)
        elif not Picture.objects.filter(item=self.item).exists():  # This is the first picture we upload
            self.is_main = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.item.item_number} picture'
