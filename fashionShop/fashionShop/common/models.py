from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from fashionShop.common.choices import CountryChoices

UserModel = get_user_model()


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

    city = models.CharField(
        verbose_name=_('city'),
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

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class Feedback(models.Model):
    author = models.CharField(
        max_length=100
    )

    comment = models.TextField()

    def __str__(self):
        return self.author


class ContactMessage(models.Model):
    name = models.CharField(
        max_length=50,
    )

    email = models.EmailField(
        max_length=50,
        null=True,
        blank=True,
    )

    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name