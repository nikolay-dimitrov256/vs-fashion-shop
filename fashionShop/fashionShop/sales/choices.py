from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ShippingChoices(TextChoices):
    SPEEDY_OFFICE = 'spof', _('SPEEDY office')
    SPEEDY_ADDRESS = 'spad', _('SPEEDY address')
    ECONT_OFFICE = 'ecof', _('ECONT office')
    ECONT_ADDRESS = 'ecad', _('ECONT address')

    @classmethod
    def is_office(cls, value):
        return value in {cls.SPEEDY_OFFICE, cls.ECONT_OFFICE}

    @classmethod
    def is_address(cls, value):
        return value in {cls.SPEEDY_ADDRESS, cls.ECONT_ADDRESS}

    @classmethod
    def courier(cls, value):
        if value.startswith('sp'):
            return 'Speedy'
        elif value.startswith('ec'):
            return 'Econt'
        return None
