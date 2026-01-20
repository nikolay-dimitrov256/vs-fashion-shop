from django.contrib import admin
from django.contrib.auth import get_user_model

from fashionShop.accounts.forms import AppUserChangeForm, AppUserCreateForm
from fashionShop.accounts.models import Profile, IpAddress

UserModel = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fields = ['first_name', 'last_name']


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None

    list_display = ['email', 'date_joined', 'last_login']
    search_fields = ['email']
    ordering = ['last_login', 'email']
    readonly_fields = ['date_joined', 'last_login',
                       'accepted_privacy_policy', 'accepted_privacy_policy_date',
                       'accepted_marketing_emails', 'accepted_marketing_emails_date']

    fieldsets = (
        ('Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('date_joined', 'last_login',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Agrrements', {'fields': ('accepted_privacy_policy', 'accepted_privacy_policy_date',
                       'accepted_marketing_emails', 'accepted_marketing_emails_date')})
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    form = AppUserChangeForm
    add_form = AppUserCreateForm


@admin.register(IpAddress)
class IpAddressAdmin(admin.ModelAdmin):
    list_display = ['ip', 'is_suspicious', 'is_banned', 'created_at']
    readonly_fields = ['ip', 'created_at', 'updated_at']