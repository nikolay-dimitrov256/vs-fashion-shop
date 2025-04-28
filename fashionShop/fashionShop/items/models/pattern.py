from django.db import models
from django.utils.translation import gettext_lazy as _


class Pattern(models.Model):
    name = models.CharField(
        _('name'),
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = _('pattern')
        verbose_name_plural = _('patterns')

    def __str__(self):
        return self.name
