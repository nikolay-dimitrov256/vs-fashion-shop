from django.db import models
from django.utils.translation import gettext_lazy as _


class Style(models.Model):
    name = models.CharField(
        max_length=20,
    )

    class Meta:
        verbose_name = _('style')
        verbose_name_plural = _('styles')

    def __str__(self):
        return self.name
