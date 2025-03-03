from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from fashionShop.accounts.managers import AppUserManager


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = AppUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class Profile(models.Model):
    user = models.OneToOneField(
        to=AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        _('first name'),
        max_length=20,
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        _('last name'),
        max_length=20,
        null=True,
        blank=True,
    )

    @property
    def full_name(self):
        first_name = self.first_name or ''
        last_name = self.last_name or ''
        full_name = f'{first_name.strip()} {last_name.strip()}'

        return full_name

    def __str__(self):
        return self.full_name.strip() or self.user.email
