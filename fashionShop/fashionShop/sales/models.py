from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'{self.user.email}\'s Cart'
