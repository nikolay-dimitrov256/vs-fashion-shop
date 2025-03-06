from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext as _


def home(request):
    context = {
        'greeting': _('Welcome to my online store'),
        'number': 12342342.69,
        'current_date': timezone.now(),
        'redirect_to': request.path
    }

    return render(request, 'common/home.html', context)
