from django.db import models
from django.utils.translation import gettext_lazy as _


class ItemCollection(models.Model):
    name = models.CharField(
        max_length=50,
    )

    position = models.SmallIntegerField(
        default=1,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('collection')
        verbose_name_plural = _('collections')
