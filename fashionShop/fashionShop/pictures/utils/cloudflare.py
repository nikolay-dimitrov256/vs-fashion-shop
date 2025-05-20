import pathlib
from urllib.parse import urlparse

import requests
from django.contrib import messages
from django.core.files.base import ContentFile
from storages.backends.s3 import S3Storage


class MediaFileStorage(S3Storage):
    # fashionShop.pictures.utils.cloudflare.MediaFileStorage
    location = 'media'


def image_file_upload_handler(instance, filepath):

    filepath = pathlib.Path(filepath).resolve()

    return f'pictures/{instance.pk}/{filepath.name}'


def migrate_image_to_r2(modeladmin, request, queryset):
    for picture in queryset:
        if picture.image_r2 or not picture.image:
            continue

        try:
            response = requests.get(picture.image.url, stream=True)

            if response.status_code == 200:
                filename = pathlib.Path(urlparse(picture.image.url).path).name
                picture.image_r2.save(filename, ContentFile(response.content), save=True)
                modeladmin.message_user(request, f"✔ Migrated {picture}", level=messages.SUCCESS)
            else:
                modeladmin.message_user(request, f"⚠ Failed to fetch {picture.image.url}", level=messages.WARNING)
        except Exception as e:
            modeladmin.message_user(request, f"✘ Error on {picture}: {e}", level=messages.ERROR)


migrate_image_to_r2.short_description = 'Migrate selected images to R2'
