from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

from django.contrib.auth import get_user_model

from fashionShop.accounts.forms import AppUserCreateForm
from fashionShop.accounts.models import Profile, IpAddress

UserModel = get_user_model()


class AppUserManagerTests(TestCase):
    def test_create_user_defaults(self):
        user = UserModel.objects.create_user(email='Test@Example.COM', password='pass')
        self.assertEqual(user.email, 'Test@example.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_success(self):
        su = UserModel.objects.create_superuser(email='admin@example.com', password='pass')
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)

    def test_create_superuser_invalid_flags(self):
        with self.assertRaises(ValueError):
            UserModel.objects.create_superuser(email='admin2@example.com', password='pass', is_staff=False)

        with self.assertRaises(ValueError):
            UserModel.objects.create_superuser(email='admin3@example.com', password='pass', is_superuser=False)

    def test_with_perm_backend_type_check(self):
        # Passing a non-string backend should raise a TypeError
        with self.assertRaises(TypeError):
            UserModel.objects.with_perm('some_perm', backend=object())


class ProfileModelTests(TestCase):
    def test_profile_created_on_user_creation(self):
        user = UserModel.objects.create_user(email='puser@example.com', password='pass')
        # Signal should create a profile automatically
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)

    def test_full_name_and_str(self):
        user = UserModel.objects.create_user(email='person@example.com', password='pass')
        profile = Profile.objects.get(user=user)

        # Initially __str__ falls back to email
        self.assertEqual(str(profile), user.email)

        profile.first_name = ' John '
        profile.last_name = ' Doe '
        profile.save()

        self.assertEqual(profile.full_name, 'John Doe')
        self.assertEqual(str(profile), 'John Doe')


class FormsAndViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Ensure the Site exists (allauth uses django.contrib.sites)
        site, _ = Site.objects.get_or_create(
            id=1,
            defaults={"domain": "example.com", "name": "example.com"},
        )

        # Create SocialApp(s) that your templates reference
        google = SocialApp.objects.create(
            provider="google",
            name="Google",
            client_id="dummy",
            secret="dummy",
            key="",
        )
        google.sites.add(site)

    def setUp(self):
        self.client = Client()

    def test_appuser_create_form_requires_privacy_policy(self):
        data = {
            'email': 'new@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            # 'accepted_privacy_policy' omitted on purpose
        }
        form = AppUserCreateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(_('You cannot register without agreeing to our Privacy Policy.'), str(form.non_field_errors()))

    def test_appuser_create_form_saves_flags_and_dates(self):
        data = {
            'email': 'market@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'accepted_privacy_policy': True,
            'accepted_marketing_emails': True,
        }
        form = AppUserCreateForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertTrue(user.accepted_privacy_policy)
        self.assertIsNotNone(user.accepted_privacy_policy_date)
        self.assertTrue(user.accepted_marketing_emails)
        self.assertIsNotNone(user.accepted_marketing_emails_date)

    def test_register_view_registers_and_logs_in(self):
        url = reverse('register')
        data = {
            'email': 'visitor@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'accepted_privacy_policy': True,
        }
        response = self.client.post(url, data, follow=True, secure=True)
        # Should end up on home page
        self.assertEqual(response.resolver_match.view_name, 'home')
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].email, 'visitor@example.com')

    def test_register_view_redirects_if_authenticated(self):
        user = UserModel.objects.create_user(email='already@example.com', password='pass')
        self.client.force_login(user)
        response = self.client.get(reverse('register'), secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_login_view_redirects_if_authenticated(self):
        user = UserModel.objects.create_user(email='already2@example.com', password='pass')
        self.client.force_login(user)
        response = self.client.get(reverse('login'), secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))


class IpAddressModelTests(TestCase):
    def test_ipaddress_str(self):
        ip = IpAddress.objects.create(ip='127.0.0.1', notes='local')
        self.assertEqual(str(ip), '127.0.0.1')
