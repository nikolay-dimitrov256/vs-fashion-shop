from django.db import models
from django.utils.translation import gettext_lazy as _


class Store(models.Model):
    id = models.IntegerField(
        primary_key=True,
    )

    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name
