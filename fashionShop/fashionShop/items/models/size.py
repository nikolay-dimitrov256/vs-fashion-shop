from django.db import models
from django.utils.translation import gettext_lazy as _


class Size(models.Model):
    size = models.CharField(
        _('size'),
        max_length=15,
        primary_key=True,
    )

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = _('size')
        verbose_name_plural = _('sizes')
        ordering = ['size']
