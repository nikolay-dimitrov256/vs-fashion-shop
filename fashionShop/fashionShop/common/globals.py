from django.utils.translation import gettext_lazy as _

BISOFT_API_URL = 'https://vilistil.com/vs/'
SPEEDY_API_URL = 'https://api.speedy.bg/v1'

CURRENCY_NAMES = {
    'BGN': _('lv'),
    'EUR': _('EUR')
}
FREE_DELIVERY_THRESHOLD = {
    'BGN': 199,
    'EUR': 101,
}

SITE_ADDRESS = 'https://vilistil.bg'
SITE_DOMAIN = 'vilistil.bg'
