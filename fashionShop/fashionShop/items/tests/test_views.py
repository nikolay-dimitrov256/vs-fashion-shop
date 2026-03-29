from decimal import Decimal

from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from fashionShop.items.models import Item, Stock, Size, ColorGroup, Category, ItemCollection
from fashionShop.items.views import ItemsListView
from fashionShop.pictures.models import Picture
from fashionShop.stores.models import Store

'''
class ViewsIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        Store.objects.create(id=0, name='Default')

    def test_item_detail_context_and_available_sizes(self):
        cat = Category.objects.create(name='dresses')
        item = Item.objects.create(item_number=30, price=Decimal('55.00'), name='Detail', slug='30-detail', category=cat)
        size = Size.objects.create(size='L')
        Stock.objects.create(item=item, size=size, quantity=5, store=Store.objects.get(id=0))
        url = reverse('item-details', kwargs={'slug': item.slug})

        resp = self.client.get(url, secure=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('available_sizes', resp.context)
        self.assertIn('other_colors', resp.context)
        self.assertIn('review_form', resp.context)

    def test_items_list_filters_by_color_and_size(self):
        store = Store.objects.get(id=0)
        cg1 = ColorGroup.objects.create(name_en='red', color_code='#f00')
        cg2 = ColorGroup.objects.create(name_en='blue', color_code='#00f')
        s1 = Size.objects.create(size='XS')
        s2 = Size.objects.create(size='S')

        i1 = Item.objects.create(item_number=40, price=Decimal('20.00'), name='C1', color_group=cg1)
        i2 = Item.objects.create(item_number=41, price=Decimal('21.00'), name='C2', color_group=cg2)

        Stock.objects.create(item=i1, size=s1, quantity=2, store=store)
        Stock.objects.create(item=i2, size=s2, quantity=3, store=store)

        url = reverse('all-items')

        # Filter by color
        resp = self.client.get(url, {'color': ['red']}, secure=True)
        self.assertEqual(resp.status_code, 200)
        items = list(resp.context['object_list'])
        self.assertIn(i1, items)
        self.assertNotIn(i2, items)

        # Filter by size
        resp2 = self.client.get(url, {'size': ['S']}, secure=True)
        self.assertEqual(resp2.status_code, 200)
        items2 = list(resp2.context['object_list'])
        self.assertIn(i2, items2)
        self.assertNotIn(i1, items2)
'''


class ItemsListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()

        # ---- Create minimal dependencies your Item might require ----
        # If your Item has required FK fields (category/collection), keep these.
        # If not required, you can remove them.
        cls.category = Category.objects.create(name="test") if hasattr(Item, "category_id") else None

        if hasattr(Item, "collection_id"):
            # Ensure 'position' exists on collection if used for ordering
            cls.collection = ItemCollection.objects.create(name="col", position=1)
        else:
            cls.collection = None

        # ---- Store: adjust to your project ----
        # If your project guarantees Store(pk=0) exists via migrations/fixtures, keep get(id=0).
        # Otherwise, create one with required fields.
        cls.store = cls._get_or_create_store()

        # Colors
        cls.cg_red = ColorGroup.objects.create(name_en="red", color_code="#f00")
        cls.cg_blue = ColorGroup.objects.create(name_en="blue", color_code="#00f")

        # Sizes
        cls.size_xs = Size.objects.create(size="XS")
        cls.size_s = Size.objects.create(size="S")
        cls.size_translated = Size.objects.create(size="EU-46")

        # Items
        base_kwargs = {
            "item_number": 100,
            "price": Decimal("20.00"),
            "name": "Item 1",
            "color_group": cls.cg_red,
        }
        if cls.category is not None:
            base_kwargs["category"] = cls.category
        if cls.collection is not None:
            base_kwargs["collection"] = cls.collection

        cls.item1 = Item.objects.create(**base_kwargs)

        base_kwargs2 = dict(base_kwargs)
        base_kwargs2.update(
            {
                "item_number": 101,
                "price": Decimal("21.00"),
                "name": "Item 2",
                "color_group": cls.cg_blue,
            }
        )
        cls.item2 = Item.objects.create(**base_kwargs2)

        # Deleted item (should never appear)
        base_kwargs3 = dict(base_kwargs)
        base_kwargs3.update(
            {
                "item_number": 102,
                "name": "Deleted",
                "deleted": True,
            }
        )
        cls.deleted_item = Item.objects.create(**base_kwargs3)

        # Stock:
        # item1 has XS in stock (translated size set -> available via translated_size path)
        cls.stock1 = Stock.objects.create(
            item=cls.item1,
            size=cls.size_xs,
            translated_size=cls.size_translated,
            quantity=2,
            store=cls.store,
        )

        # item2 has S in stock (translated_size is NULL -> available via size path)
        cls.stock2 = Stock.objects.create(
            item=cls.item2,
            size=cls.size_s,
            quantity=3,
            store=cls.store,
        )

        # item2 also has XS but quantity 0 (should NOT make it appear for XS)
        cls.stock3 = Stock.objects.create(
            item=cls.item2,
            size=cls.size_xs,
            quantity=0,
            store=cls.store,
        )

        # Pictures: ensure prefetch picks only first
        # (Assumes Picture has FK to Item via related_name='pictures')
        Picture.objects.create(item=cls.item1)  # first
        Picture.objects.create(item=cls.item1)  # second

    @classmethod
    def _get_or_create_store(cls):
        # Try to use existing store (common in projects with seed data)
        store, _ = Store.objects.get_or_create(pk=0)

        return store



    def _get_view_and_response(self, query_params=None):
        """
        Build a request and return (view_instance, response) without rendering templates.
        """
        query_params = query_params or {}
        request = self.factory.get("/items/", data=query_params)
        view = ItemsListView()
        view.request = request
        view.args = ()
        view.kwargs = {}

        # Get queryset and context without rendering
        qs = view.get_queryset()
        view.object_list = qs
        context = view.get_context_data(object_list=qs)
        return view, qs, context

    def test_context_contains_expected_keys_and_query_params_without_page(self):
        view, qs, context = self._get_view_and_response({"page": "2", "color": ["red", "blue"], "show": "1"})

        self.assertIn("colors", context)
        self.assertIn("sizes", context)
        self.assertIn("paginate_by", context)
        self.assertIn("query_params", context)

        # page removed from query_params
        self.assertNotIn("page", context["query_params"])
        self.assertEqual(context["query_params"].getlist("color"), ["red", "blue"])

        # paginate_by comes from GET['show'] (note: your method returns a string)
        self.assertEqual(context["paginate_by"], "1")

    def test_context_sizes_are_distinct_and_ordered(self):
        _, _, context = self._get_view_and_response()

        # context['sizes'] is a ValuesListQuerySet of Stock.size IDs
        size_ids = list(context["sizes"])
        self.assertEqual(size_ids, sorted(set(size_ids)))

    def test_queryset_excludes_deleted_items(self):
        _, qs, _ = self._get_view_and_response()
        self.assertIn(self.item1, qs)
        self.assertIn(self.item2, qs)
        self.assertNotIn(self.deleted_item, qs)

    def test_queryset_filters_by_color_name_en(self):
        _, qs, _ = self._get_view_and_response({"color": ["red"]})
        self.assertIn(self.item1, qs)
        self.assertNotIn(self.item2, qs)

    def test_queryset_filters_by_size_including_translated_size(self):
        # Selecting "EU-46" should match item1 via stock.translated_size.size == "EU-46"
        _, qs, _ = self._get_view_and_response({"size": ["EU-46"]})
        self.assertIn(self.item1, qs)
        self.assertNotIn(self.item2, qs)

    def test_queryset_filters_by_size_when_translated_is_null(self):
        # Selecting "S" should match item2 via stock.size.size == "S" and translated_size is null
        _, qs, _ = self._get_view_and_response({"size": ["S"]})
        self.assertIn(self.item2, qs)
        self.assertNotIn(self.item1, qs)

    def test_queryset_size_filter_requires_quantity_gt_zero(self):
        # item2 has XS stock with quantity=0. That must NOT include item2.
        _, qs, _ = self._get_view_and_response({"size": ["EU-46"]})
        self.assertIn(self.item1, qs)      # item1 has XS qty=2
        self.assertNotIn(self.item2, qs)   # item2 XS is qty=0

    def test_queryset_prefetches_main_picture_list_first_only(self):
        # Run through queryset evaluation so prefetch executes
        _, qs, _ = self._get_view_and_response()
        items = list(qs)

        # Find item1 and ensure it has main_picture_list with at most 1 pic
        item1 = next(i for i in items if i.pk == self.item1.pk)
        self.assertTrue(hasattr(item1, "main_picture_list"))
        self.assertLessEqual(len(item1.main_picture_list), 1)
