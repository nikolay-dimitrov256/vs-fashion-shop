from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import TemplateView


def home(request):
    context = {
        'greeting': _('Welcome to my online store'),
        'number': 12342342.69,
        'current_date': timezone.now(),
        'redirect_to': request.path
    }

    return render(request, 'common/test.html', context)


class HomeView(TemplateView):
    template_name = 'common/home.html'


class CategoryView(TemplateView):
    template_name = 'common/categories.html'


class SingleView(TemplateView):
    template_name = 'common/single.html'


class ContactView(TemplateView):
    template_name = 'common/contact.html'
