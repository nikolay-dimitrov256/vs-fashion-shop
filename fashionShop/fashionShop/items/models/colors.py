from django.db import models
from django.utils.translation import gettext_lazy as _


class ColorGroup(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
    )

    color_code = models.CharField(
        max_length=10,
    )

    class Meta:
        verbose_name = _('color group')
        verbose_name_plural = _('color groups')

    def __str__(self):
        return self.name
