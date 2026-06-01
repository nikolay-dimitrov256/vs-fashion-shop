from decimal import Decimal
from datetime import datetime, timezone
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site
from django.test import RequestFactory, TestCase
from django.utils.translation import gettext as _

from fashionShop.accounts.models import IpAddress
from fashionShop.common.choices import CountryChoices
from fashionShop.common.forms import AddressForm
from fashionShop.common.utils import get_absolute_url
from fashionShop.items.models.item import Item
from fashionShop.items.models.online_items import CartItem, OrderItem
from fashionShop.items.models.size import Size
from fashionShop.sales.choices import ShippingChoices, StatusChoices
from fashionShop.sales.forms import ShippingOrderForm
from fashionShop.sales.models import Cart, OnlineOrder
from fashionShop.sales.tasks import send_bisoft_report, send_sms
from fashionShop.sales.utils import fill_order_from_cart_empty_cart, get_bisoft_column

UserModel = get_user_model()


class OnlineOrderModelTests(TestCase):
    def setUp(self):
        Site.objects.update_or_create(
            pk=1,
            defaults={
                'domain': 'example.com',
                'name': 'example.com',
            }
        )
        self.user = UserModel.objects.create_user(
            email='customer@example.com',
            password='password123',
        )

    @patch('fashionShop.sales.models.timezone.now')
    def test_save_generates_sequential_order_code_by_month(self, mock_now):
        mock_now.return_value = datetime(2026, 3, 5, 12, 0, 0, tzinfo=timezone.utc)

        first_order = OnlineOrder.objects.create(phone='0881234567')
        second_order = OnlineOrder.objects.create(phone='0887654321')

        self.assertEqual(first_order.order_code, '2603490001')
        self.assertEqual(second_order.order_code, '2603490002')

    def test_full_name_returns_combined_name_or_none(self):
        order = OnlineOrder.objects.create(
            phone='0881234567',
            first_name='John',
            last_name='Doe',
        )
        self.assertEqual(order.full_name, 'John Doe')

        blank_name_order = OnlineOrder.objects.create(phone='0881112222')
        self.assertIsNone(blank_name_order.full_name)

    def test_status_message_returns_pending_and_completed_messages(self):
        item = Item.objects.create(
            item_number=200,
            name='Test Product',
            slug='test-product',
            price=Decimal('10.00'),
        )
        size = Size.objects.create(size='M')
        order = OnlineOrder.objects.create(
            phone='0881234567',
            first_name='Jane',
            last_name='Doe',
            status=StatusChoices.COMPLETED,
        )
        OrderItem.objects.create(
            item=item,
            order=order,
            size=size,
            quantity=1,
            at_price=Decimal('10.00'),
            total_price=Decimal('10.00'),
        )
        absolute_url = get_absolute_url('item-details', kwargs={'slug': item.slug})

        self.assertIn('Вили Стил:', order.status_message)
        self.assertIn(absolute_url, order.status_message)
        self.assertIn('test-product', order.status_message)

    def test_infobip_phone_normalizes_international_and_local_numbers(self):
        order = OnlineOrder.objects.create(phone='+35988 123 4567')
        self.assertEqual(order.infobip_phone, '359881234567')

        order.phone = '0881234567'
        order.save()
        self.assertEqual(order.infobip_phone, '359881234567')

        order.phone = 'invalid number'
        order.save()
        self.assertEqual(order.infobip_phone, '')

    def test_ip_properties_reflect_related_ip_record(self):
        ip = IpAddress.objects.create(
            ip='203.0.113.1',
            is_suspicious=True,
            is_banned=True,
            notes='test-ip',
        )
        order = OnlineOrder.objects.create(phone='0881234567', ip=ip)

        self.assertTrue(order.ip_is_suspicious)
        self.assertTrue(order.ip_is_banned)

    def test_str_returns_order_number(self):
        order = OnlineOrder.objects.create(phone='0881234567')
        self.assertEqual(str(order), f'Order number {order.pk}')


class ShippingOrderFormTests(TestCase):
    def test_missing_shipping_method_makes_form_invalid(self):
        form = ShippingOrderForm(
            data={
                'phone': '0881234567',
                'email': 'test@example.com',
                'first_name': 'Alice',
                'last_name': 'Smith',
            },
            address_form=AddressForm(data={}),
        )

        self.assertFalse(form.is_valid())
        self.assertIn(_('Please select a shipping method.'), form.errors.get('shipping_method', []))

    def test_office_delivery_requires_town_and_office(self):
        form = ShippingOrderForm(
            data={
                'phone': '0881234567',
                'shipping_method': ShippingChoices.SPEEDY_OFFICE,
                'first_name': 'Alice',
                'last_name': 'Smith',
                'town': '',
                'office': '',
            },
            address_form=AddressForm(data={}),
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
        _('Please provide both town and office for office delivery.'),
            form.non_field_errors(),
        )

    def test_address_delivery_requires_valid_address_form(self):
        form = ShippingOrderForm(
            data={
                'phone': '0881234567',
                'shipping_method': ShippingChoices.ECONT_ADDRESS,
                'first_name': 'Alice',
                'last_name': 'Smith',
            },
            address_form=AddressForm(data={}),
        )

        self.assertFalse(form.is_valid())
        self.assertFalse(form.address_form.is_valid())

    def test_address_delivery_saves_address(self):
        address_form = AddressForm(
            data={
                'country': CountryChoices.BULGARIA,
                'province': 'Sofia',
                'city': 'Sofia',
            }
        )
        form = ShippingOrderForm(
            data={
                'phone': '0881234567',
                'shipping_method': ShippingChoices.SPEEDY_ADDRESS,
                'first_name': 'Alice',
                'last_name': 'Smith',
            },
            address_form=address_form,
        )

        self.assertTrue(address_form.is_valid(), address_form.errors)
        self.assertTrue(form.is_valid(), form.errors)
        order = form.save()
        self.assertIsNotNone(order.address)
        self.assertEqual(order.address.city, 'Sofia')

    def test_office_delivery_does_not_store_address(self):
        address_form = AddressForm(
            data={
                'province': 'Sofia',
                'city': 'Sofia',
            }
        )
        form = ShippingOrderForm(
            data={
                'phone': '0881234567',
                'shipping_method': ShippingChoices.SPEEDY_OFFICE,
                'first_name': 'Alice',
                'last_name': 'Smith',
                'town': 'Sofia',
                'office': 'Office 1',
            },
            address_form=address_form,
        )

        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertIsNone(order.address)


class FillOrderFromCartEmptyCartTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            email='cartuser@example.com',
            password='password123',
        )
        self.item = Item.objects.create(
            item_number=300,
            name='Cart Product',
            slug='cart-product',
            price=Decimal('15.00'),
        )
        self.size = Size.objects.create(size='L')

    def test_authenticated_user_cart_items_are_moved_to_order_and_cart_is_emptied(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            item=self.item,
            cart=cart,
            size=self.size,
            quantity=2,
        )

        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        order = OnlineOrder.objects.create(phone='0881234567')

        created_items = fill_order_from_cart_empty_cart(request, order)

        self.assertEqual(len(created_items), 1)
        self.assertEqual(order.order_items.count(), 1)
        self.assertEqual(CartItem.objects.filter(cart=cart).count(), 0)

    def test_anonymous_user_session_cart_is_converted_to_order_items(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()

        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        request.session['cart'] = {
            str(self.item.item_number): {
                self.size.size: '3',
            }
        }

        order = OnlineOrder.objects.create(phone='0881234567')

        created_items = fill_order_from_cart_empty_cart(request, order)

        self.assertEqual(len(created_items), 1)
        self.assertEqual(order.order_items.count(), 1)
        self.assertEqual(request.session['cart'], {})


class SalesTasksTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            item_number=400,
            name='Report Item',
            slug='report-item',
            price=Decimal('25.00'),
        )
        self.size = Size.objects.create(size='S')
        self.order = OnlineOrder.objects.create(
            phone='0881234567',
            first_name='Kris',
            last_name='Anderson',
            total=Decimal('50.00'),
            shipping_method=ShippingChoices.ECONT_OFFICE,
        )
        OrderItem.objects.create(
            item=self.item,
            order=self.order,
            size=self.size,
            quantity=2,
            at_price=Decimal('25.00'),
            total_price=Decimal('50.00'),
        )

    @patch('fashionShop.sales.tasks.requests.post')
    def test_send_bisoft_report_returns_true_and_saves_flag(self, mock_post):
        response = Mock()
        response.status_code = 200
        response.text = '{}'
        response.json.return_value = {'success': True}
        mock_post.return_value = response

        result = send_bisoft_report(self.order.pk, save=True)

        self.assertTrue(result)
        self.order.refresh_from_db()
        self.assertTrue(self.order.bisoft_report_sent)
        posted_json = mock_post.call_args[1]['json']
        self.assertEqual(posted_json['user']['doc_num'], self.order.order_code)
        self.assertEqual(posted_json['basket'][str(self.item.pk)]['sizes'][get_bisoft_column(self.size, self.item)], 2)

    @patch('fashionShop.sales.tasks.requests.post')
    def test_send_bisoft_report_returns_false_on_request_exception(self, mock_post):
        mock_post.side_effect = Exception('network error')

        result = send_bisoft_report(self.order.pk, save=True)

        self.assertFalse(result)

    @patch('fashionShop.sales.tasks.requests.post')
    def test_send_sms_returns_payload_response(self, mock_post):
        response = Mock()
        response.json.return_value = {'messages': []}
        mock_post.return_value = response

        result = send_sms('359881234567', 'Hello')

        self.assertEqual(result, {'messages': []})
        mock_post.assert_called_once()
        self.assertIn('sms/3/messages', mock_post.call_args[0][0])

    def test_send_sms_returns_none_if_missing_to_or_message(self):
        self.assertIsNone(send_sms('', 'Hello'))
        self.assertIsNone(send_sms('359881234567', ''))
