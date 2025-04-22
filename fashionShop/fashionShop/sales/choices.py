from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ShippingChoices(TextChoices):
    SPEEDY_OFFICE = 'spof', _('SPEEDY office')
    SPEEDY_ADDRESS = 'spad', _('SPEEDY, address')
    ECONT_OFFICE = 'ecof', _('ECONT office')
    ECONT_ADDRESS = 'ecad', _('ECONT address')
