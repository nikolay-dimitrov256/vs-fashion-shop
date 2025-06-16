from fashionShop.common import globals
from fashionShop.common.forms import SearchForm


def global_variables(request):
    gl_vars = {
        'SITE_ADDRESS': globals.SITE_ADDRESS
    }

    return gl_vars


def search_form(request):
    return {
        'search_form': SearchForm(request.GET or None)
    }
