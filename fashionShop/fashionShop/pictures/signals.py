from cloudinary import uploader
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from fashionShop.pictures.models import Picture, ReviewPicture


@receiver(pre_delete, sender=Picture)
def delete_picture_files(sender, instance: Picture, **kwargs):
    if instance.image:
        public_id = instance.image.public_id

        if public_id:
            uploader.destroy(public_id)

    if instance.image_r2:
        instance.image_r2.delete(save=False)


@receiver(pre_delete, sender=ReviewPicture)
def delete_review_picture_files(sender, instance: ReviewPicture, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
