from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    author = models.CharField(
        _('full name'),
        max_length=100,
    )

    rating = models.PositiveSmallIntegerField(
        _('rating'),
        validators=[
            MinValueValidator(1, message=_('The review score cannot be below 1.')),
            MaxValueValidator(5, message=_('The review score cannot be above 5.')),
        ]
    )

    title = models.CharField(
        _('title'),
        max_length=100,
        null=True,
        blank=True,
    )

    content = models.TextField(
        _('text'),
        validators=[
            MinLengthValidator(5, message=_('Please write something.'))
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    item = models.ForeignKey(
        to='items.Item',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']
