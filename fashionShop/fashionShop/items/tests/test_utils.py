from decimal import Decimal
from unittest.mock import patch, Mock

from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage

from fashionShop.items.models import Item, Stock, Size, ItemCollection
from fashionShop.items import utils as items_utils
from fashionShop.stores.models import Store


class UtilsTests(TestCase):
    def setUp(self):
        Store.objects.create(id=0, name='Default')

    def test_make_set_collection_action_updates_items_and_adds_message(self):
        collection = ItemCollection.objects.create(name='TestCollection')
        i1 = Item.objects.create(item_number=20, price=Decimal('10.00'))
        i2 = Item.objects.create(item_number=21, price=Decimal('12.00'))

        action = items_utils.make_set_collection_action(collection)

        factory = RequestFactory()
        request = factory.post('/')
        # Attach messages framework to the request
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Call the action
        action(None, request, Item.objects.filter(item_number__in=[20, 21]))

        i1.refresh_from_db()
        i2.refresh_from_db()
        self.assertEqual(i1.collection, collection)
        self.assertEqual(i2.collection, collection)

        # Ensure a success message was added
        storage = list(messages)
        self.assertTrue(any('items were set to collection' in str(m) or 'items were set to collection' in m.message for m in storage))
