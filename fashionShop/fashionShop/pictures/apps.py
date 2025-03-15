from django.apps import AppConfig


class PicturesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fashionShop.pictures'

    def ready(self):
        import fashionShop.pictures.signals
