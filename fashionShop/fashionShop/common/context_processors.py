from fashionShop.common import globals
from fashionShop.common.forms import SearchForm
from fashionShop.common.globals import is_black_friday
from fashionShop.items.models import Item


def global_variables(request):
    gl_vars = {
        'SITE_ADDRESS': globals.SITE_ADDRESS,
        'is_black_friday': is_black_friday,
        # 'black_friday_discount_percent': black_friday_discount_percent
        'max_black_percent': Item.objects.values_list('black_percent', flat=True).order_by('-black_percent').first()
    }

    return gl_vars


def search_form(request):
    return {
        'search_form': SearchForm(request.GET or None)
    }
