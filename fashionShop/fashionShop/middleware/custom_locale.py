from django.middleware.locale import LocaleMiddleware
from django.utils import translation
from django.conf import settings


class CustomLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        # Try language from session
        language = request.session.get('django_language')
        if not language:
            # Try language from cookie
            language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        if not language:
            # Fall back to default language (Bulgarian)
            language = settings.LANGUAGE_CODE

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()