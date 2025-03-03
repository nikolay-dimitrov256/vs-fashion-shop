from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fashionShop.accounts'

    def ready(self):
        import fashionShop.accounts.signals
