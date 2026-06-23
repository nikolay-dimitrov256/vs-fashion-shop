from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from fashionShop.common.globals import SITE_DOMAIN
from fashionShop.pictures.utils.cloudflare import image_file_upload_handler, review_image_upload_handler


class Picture(models.Model):
    image_r2 = models.ImageField(
        upload_to=image_file_upload_handler,
        null=True,
        blank=True,
    )

    is_main = models.BooleanField(
        default=False,
    )

    is_detail = models.BooleanField(
        default=False,
    )

    description = models.TextField(
        _('description'),
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    item = models.ForeignKey(
        verbose_name=_('item'),
        to='items.Item',
        on_delete=models.CASCADE,
        related_name='pictures'
    )

    class Meta:
        ordering = ['-is_main', 'is_detail', 'created_at']

    @property
    def image_url(self):
        return f'https://media.{SITE_DOMAIN}/{self.image_r2.name}'

    def save(self, *args, **kwargs):
        if self.is_main:
            Picture.objects.filter(item=self.item, is_main=True).exclude(id=self.id).update(is_main=False)
        elif not Picture.objects.filter(item=self.item).exists():  # This is the first picture we upload
            self.is_main = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.item.item_number} picture'


class ReviewPicture(models.Model):
    image = models.ImageField(
        upload_to=review_image_upload_handler,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    review = models.ForeignKey(
        to='reviews.Review',
        on_delete=models.CASCADE,
        related_name='pictures',
    )

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')  # Normalize format

            max_width = 1200
            if img.width > max_width:
                # Calculate new height to preserve aspect ratio
                w_percent = max_width / float(img.width)
                new_height = int((float(img.height) * float(w_percent)))
                img = img.resize((max_width, new_height), Image.LANCZOS)

            # Save to buffer
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)

            # Replace original image
            self.image = ContentFile(buffer.read(), name=self.image.name)

        super().save(*args, **kwargs)
