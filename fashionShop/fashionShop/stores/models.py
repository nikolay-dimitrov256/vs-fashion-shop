from django.db import models


class Store(models.Model):
    id = models.IntegerField(
        primary_key=True,
    )

    name = models.CharField(
        max_length=50,
        unique=True,
    )

    # address = models.OneToOneField(
    #     to='common.Address',
    #     on_delete=models.CASCADE,
    # )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name
