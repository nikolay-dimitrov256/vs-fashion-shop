from django.db import models
from django.utils.translation import gettext_lazy as _

from fashionShop.common.choices import CountryChoices


class Address(models.Model):
    country = models.CharField(
        verbose_name=_('country'),
        max_length=20,
        choices=CountryChoices.choices,
        default=CountryChoices.BULGARIA,
    )

    province = models.CharField(
        verbose_name=_('province'),
        max_length=20,
    )

    town = models.CharField(
        verbose_name=_('town'),
        max_length=20,
    )

    postal_code = models.CharField(
        verbose_name=_('postal code'),
        max_length=20,
    )

    street = models.CharField(
        verbose_name=_('street'),
        max_length=50,
        null=True,
        blank=True,
    )

    number = models.CharField(
        verbose_name=_('number'),
        max_length=10,
        null=True,
        blank=True,
    )

    building = models.CharField(
        verbose_name=_('building'),
        max_length=10,
        null=True,
        blank=True,
    )

    entrance = models.CharField(
        verbose_name=_('entrance'),
        max_length=5,
        null=True,
        blank=True,
    )

    apartment = models.CharField(
        verbose_name=_('apartment'),
        max_length=10,
        null=True,
        blank=True,
    )

    store = models.OneToOneField(
        to='stores.Store',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
