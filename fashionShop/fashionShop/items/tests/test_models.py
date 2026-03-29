from decimal import Decimal

from django.test import TestCase

from fashionShop.items.models import Item, Stock, Size
from fashionShop.stores.models import Store


class ItemModelTests(TestCase):
    def setUp(self):
        # Ensure store with id=0 exists because Stock defaults to store=0
        Store.objects.create(id=0, name='Default')

    def test_is_discounted_and_prices(self):
        item = Item.objects.create(item_number=1, price=Decimal('100.00'), discount_price=Decimal('80.00'), name='Test')

        self.assertTrue(item.is_discounted)
        self.assertEqual(item.discount, Decimal('20.00'))
        # EURO_RATE is 1.95583 from settings -> discount_bgn
        self.assertEqual(item.discount_bgn.quantize(Decimal('.01')), (Decimal('20.00') * Decimal('1.95583')).quantize(Decimal('.01')))
        self.assertEqual(item.final_price, Decimal('80.00'))
        self.assertEqual(item.price_bgn.quantize(Decimal('.01')), (Decimal('100.00') * Decimal('1.95583')).quantize(Decimal('.01')))

    def test_black_price_calculation(self):
        item = Item.objects.create(item_number=2, price=Decimal('100.00'), discount_price=Decimal('90.00'), name='BF')
        # black_price reduces the (discount_price if discounted else price) by 10%
        expected = (Decimal('90.00') - (Decimal('90.00') * Decimal('0.10'))).quantize(Decimal('.01'))
        self.assertEqual(item.black_price, expected)

    def test_stock_effective_size_and_available_sizes(self):
        s_small = Size.objects.create(size='40')
        s_translated = Size.objects.create(size='60')
        m_medium = Size.objects.create(size='46')
        item = Item.objects.create(item_number=3, price=Decimal('50.00'), name='SizeTest')
        store = Store.objects.get(id=0)

        # Create stock with translated size
        stock1 = Stock.objects.create(item=item, size=s_small, translated_size=s_translated, quantity=2, store=store)
        # Create stock with zero quantity - should not appear in available sizes
        stock2 = Stock.objects.create(item=item, size=m_medium, quantity=0, store=store)

        self.assertEqual(stock1.effective_size, s_translated)

        available = list(item.get_available_sizes())
        self.assertIn(s_translated, available)
        self.assertNotIn(s_small, available)
        self.assertNotIn(m_medium, available)
