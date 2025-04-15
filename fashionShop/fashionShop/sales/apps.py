from django.apps import AppConfig


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fashionShop.sales'

    def ready(self):
        import fashionShop.sales.signals
