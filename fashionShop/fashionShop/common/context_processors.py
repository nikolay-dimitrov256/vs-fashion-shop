from fashionShop.common import globals


def global_variables(request):
    gl_vars = {
        'SITE_ADDRESS': globals.SITE_ADDRESS
    }

    return gl_vars
