from datetime import datetime, timedelta

from django.db.models import OuterRef, Subquery, Prefetch, Q, Avg, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from fashionShop.common.utils import get_absolute_url
from fashionShop.items.models import Item, ColorGroup, Stock, Size, SubCategory
from fashionShop.pictures.forms import ReviewPictureFormSet
from fashionShop.pictures.models import Picture
from fashionShop.reviews.forms import ReviewCreateForm


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/single.html'

    def get_object(self, queryset=None):
        # item = super().get_object(queryset)
        item = get_object_or_404(
            Item.objects
            .annotate(review_avg=Avg('reviews__rating'))
            .select_related('category', 'sub_category', 'pattern', 'color_group')
            .prefetch_related(
                'linked_items',
                'linked_items__pictures',
                'pictures',
                'reviews',
                'reviews__pictures'
            ),
            slug=self.kwargs['slug']
        )

        item.detail_pictures = item.pictures.filter(is_detail=True)
        if item.description:
            item.description = item.description.split(';')
            if len(item.description) == 1:
                item.description = item.description[0].split('\n')

        item.additional_info = item.additional_info.split(';') if item.additional_info else []

        # item.data_layer = {
        #     'value': item.price_eur,
        #     'item_id': item.pk,
        #     'item_name': item.name,
        #     'item_category': item.category.name,
        #     'price': item.price_eur,
        # }

        return item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['available_sizes'] = (
            Stock.objects
            .filter(item=self.object, quantity__gt=0)
            .annotate(effective_size=Coalesce('translated_size', 'size'))
            .values_list('effective_size', flat=True)
            .order_by('size__size')
            .distinct()
        )
        context['other_colors'] = (
            Item.objects
            .exclude(Q(deleted=True) | Q(pk=self.object.pk))
            .filter(pattern=self.object.pattern, pattern__isnull=False)
        )
        context['review_avg'] = round(self.object.review_avg or 0)
        context['review_form'] = ReviewCreateForm(self.request.POST or None)
        context['formset'] = ReviewPictureFormSet(self.request.POST or None, self.request.FILES or None)
        context['canonical_url'] = get_absolute_url('item-details', kwargs={'slug': self.object.slug})

        return context


class ItemsListView(ListView):
    model = Item
    template_name = 'items/category.html'
    view_name = 'all-items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        context['colors'] = ColorGroup.objects.all()
        context['sizes'] = Stock.objects.values_list('size', flat=True).order_by('size').distinct()
        context['paginate_by'] = self.get_paginate_by(self.queryset)

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = query_params
        context['canonical_url'] = get_absolute_url(self.view_name)
        context['meta_title'] = self.meta_title
        context['meta_description'] = self.meta_description

        return context

    def get_queryset(self):
        items = (
            Item.objects
            .prefetch_related(
                Prefetch(
                    'pictures',
                    queryset=Picture.objects.all()[:1],  # Only fetch the first image
                    to_attr='main_picture_list'
                )
            )
            .exclude(deleted=True)
        )

        selected_colors = self.request.GET.getlist('color')
        if selected_colors:
            items = items.filter(color_group__name_en__in=selected_colors)

        selected_sizes = self.request.GET.getlist('size')
        if selected_sizes:
            items = items.filter(
                Q(stock__translated_size__size__in=selected_sizes) |
                Q(stock__translated_size__isnull=True, stock__size__size__in=selected_sizes),
                stock__quantity__gt=0,
            )

        return items.order_by('-is_new', 'collection__position', '-created_at').distinct()

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('show', 12)

        return paginate_by

    @property
    def meta_title(self):
        return 'Дамски дрехи - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Дамски дрехи от българския производител Вили Стил подходящи за всякакви случаи. '
                'Разнообразие от цветове и размери. За запитвания и поръчки - 0886531811')


class PantsListView(ItemsListView):
    template_name = 'items/pants.html'
    view_name = 'pants'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='pants')

        return items

    @property
    def meta_title(self):
        return 'Дамски панталони спортно елегантни - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Вземете си панталон от Вили Стил, за да се чувствате комфортно навсякъде. Голямо разнообразие '
                'от цветове и размери. За запитвания и поръчки - 0886531811')


class SkirtsListView(ItemsListView):
    template_name = 'items/skirts.html'
    view_name = 'skirts'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='skirts')

        return items

    @property
    def meta_title(self):
        return 'Дамски поли - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return 'Разгледайте дамски поли от българския производител Вили Стил. За запитвания и поръчки - 0886531811'


class DressesListView(ItemsListView):
    template_name = 'items/dresses.html'
    view_name = 'dresses'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='dresses')

        return items

    @property
    def meta_title(self):
        return 'Стилни дамски рокли - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте дамски рокли от българския производител Вили Стил. Подходящи за ежедневни разходки, '
                'офис, специални случаи. За запитвания и поръчки - 0886531811')


class ShirtsListView(ItemsListView):
    template_name = 'items/shirts.html'
    view_name = 'shirts'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='shirts')

        return items

    @property
    def meta_title(self):
        return 'Дамски ризи спортно елегантни и официални Онлайн Цени Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте дамски ризи от българския производител Вили Стил. Имаме голямо разнообразие от '
                'цветове и размери за всякакви поводи. За поръчки - 0886531811')


class BlousesListView(ItemsListView):
    template_name = 'items/blouses.html'
    view_name = 'blouses'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='blouses')

        return items

    @property
    def meta_title(self):
        return 'Стилни дамски блузи - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте предложенията за блузи от българския производител Вили Стил. Имаме голямо разнообразие '
                'от цветове и размери за всякакви поводи. За поръчки - 0886531811')


class TunicsListView(ItemsListView):
    template_name = 'items/tunics.html'
    view_name = 'tunics'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='tunics')

        return items

    @property
    def meta_title(self):
        return 'Дамски туники спортно-елегантни - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return 'Разгледайте дамски туники от българския производител Вили Стил. За запитвания и поръчки - 0886531811'


class BlazersListView(ItemsListView):
    template_name = 'items/blazers.html'
    view_name = 'blazers'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='blazers')

        return items

    @property
    def meta_title(self):
        return 'Стилни дамски сака - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте дамски сака и блейзъри от българския производител Вили Стил. Имаме голямо разнообразие '
                'от цветове и размери. За запитвания и поръчки - 0886531811')


class SuitsListView(ItemsListView):
    template_name = 'items/suits.html'
    view_name = 'suits'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='suits')

        return items

    @property
    def meta_title(self):
        return 'Дамски костюми - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return 'Разгледайте дамски костюми от българския производител Вили Стил. За запитвания и поръчки - 0886531811'


class JacketsListView(ItemsListView):
    template_name = 'items/jackets.html'
    view_name = 'jackets'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='jackets')

        return items

    @property
    def meta_title(self):
        return 'Стилни дамски якета - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте дамски якета от българския производител Вили Стил. Имаме голямо разнообразие от '
                'цветове и размери. За запитвания и поръчки - 0886531811')


class CoatsListView(ItemsListView):
    template_name = 'items/coats.html'
    view_name = 'coats'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='coats')

        return items

    @property
    def meta_title(self):
        return 'Стилни дамски манта - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте дамски манта от българския производител Вили Стил. Имаме голямо разнообразие от цветове '
                'и размери. За запитвания и поръчки - 0886531811')


class VestsListView(ItemsListView):
    template_name = 'items/vests.html'
    view_name = 'vests'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='vests')

        return items

    @property
    def meta_title(self):
        return 'Стилни дамски елеци - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return 'Разгледайте дамски елеци от българския производител Вили Стил. За запитвания и поръчки - 0886531811'


class TankTopsListView(ItemsListView):
    template_name = 'items/tank-tops.html'
    view_name = 'underwear'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='underwear')

        return items

    @property
    def meta_title(self):
        return 'Дамски потници - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return 'Разгледайте дамски потници от българския производител Вили Стил. За запитвания и поръчки - 0886531811'


class SetsListView(ItemsListView):
    template_name = 'items/sets.html'
    view_name = 'classic'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='classic')

        return items

    @property
    def meta_title(self):
        return 'Дамски комплекти спортно елегантни - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Вземете си комплект от Вили Стил, за да се чувствате комфортно навсякъде. Голямо разнообразие от '
                'цветове и размери. За запитвания и поръчки - 0886531811')


class CardigansListView(ItemsListView):
    template_name = 'items/tank-tops.html'
    view_name = 'cardigans'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(category__name_en='cardigans')

        return items

    @property
    def meta_title(self):
        return 'Дамски жилетки - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте дамски жилетки от българския производител Вили Стил. Имаме голямо разнообразие от '
                'цветове и размери. За запитвания и поръчки - 0886531811')


class ElegantListView(ItemsListView):
    template_name = 'items/elegant.html'
    view_name = 'elegant'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(style__name__iexact='elegant')

        return items

    @property
    def meta_title(self):
        return 'Спортно елегантни дамски дрехи - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте спортно елегантни дрехи от Вили Стил. Имаме голямо разнообразие от цветове и размери '
                'за всякакви поводи. За поръчки - 0886531811')


class OfficeListView(ItemsListView):
    template_name = 'items/office.html'
    view_name = 'office'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(style__name__iexact='office')

        return items

    @property
    def meta_title(self):
        return 'Дамски офис дрехи - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Работата е удоволствие, когато се върши със стил. Разгледайте офис тоалетите ни за жени, за да '
                'покажете стила си на работното място. За поръчки - 0886531811')


class OfficialListView(ItemsListView):
    template_name = 'items/official.html'
    view_name = 'official'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(style__name__iexact='official')

        return items

    @property
    def meta_title(self):
        return 'Официални дрехи за жени - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Възползвайте се от предложенията ни за официални дамски дрехи, за да сияете на предстоящото събитие. '
                'За въпроси и поръчки - 0886531811')


class SearchView(ItemsListView):
    template_name = 'items/search.html'
    view_name = 'search'

    def get_queryset(self):
        items = super().get_queryset()

        search = self.request.GET.get('search', '').strip()
        query = (Q(name__icontains=search) | Q(name_en__icontains=search)
                 | Q(description__icontains=search) | Q(description_en__icontains=search))

        if search.isdigit():
            query |= Q(pk=search)

        items = items.filter(query)

        return items


class BestsellersListView(ItemsListView):
    template_name = 'items/bestsellers.html'
    view_name = 'bestsellers'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.annotate(sales=Sum('order_items__quantity')).filter(sales__gte=5).order_by('-sales')

        return items

    @property
    def meta_title(self):
        return 'Най-продавани дрехи | Вили Стил'

    @property
    def meta_description(self):
        return 'Най-продаваните ни изделия. За запитвания и поръчки - 0886531811'


class NewItemsListView(ItemsListView):
    template_name = 'items/new.html'
    view_name = 'new'

    def get_queryset(self):
        items = super().get_queryset()

        items = items.filter(is_new=True)

        return items

    @property
    def meta_title(self):
        return 'Нови предложения - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте новите предложения на българския производител Вили Стил. За запитвания и поръчки - '
                '0886531811')


class MaxSizeListView(ItemsListView):
    template_name = 'items/max-size.html'
    view_name = 'max-size'

    def get_queryset(self):
        items = super().get_queryset()

        max_sizes = ['52', '54', '56', '58', '60', '62', '64', '66', '68', '70']

        query = (
            Q(stock__translated_size__size__in=max_sizes) |
            Q(stock__translated_size__size__isnull=True, stock__size__size__in=max_sizes)
        ) & Q(stock__quantity__gt=0)

        items = items.filter(query)

        return items

    @property
    def meta_title(self):
        return 'Дамски дрехи големи размери - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Стилни дамски дрехи в големи размери – открий своя модел и се почувствай уверено. Бърза доставка '
                'и коректно обслужване.')


class FallWinterListView(ItemsListView):
    template_name = 'items/fall-winter.html'
    view_name = 'fall-winter'

    def get_queryset(self):
        items = super().get_queryset()

        query = Q(collection__name='есен/зима') | Q(collection__name='пролет/есен')
        items = items.filter(query)

        return items

    @property
    def meta_title(self):
        return 'Колекция есен/зима - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте предложенията за сезон есен/зима на българския производител на дамски дрехи Вили Стил. '
                'За запитвания и поръчки - 0886531811')


class SpringSummerListView(ItemsListView):
    template_name = 'items/spring-summer.html'
    view_name = 'spring-summer'

    def get_queryset(self):
        items = super().get_queryset()

        query = Q(collection__name='пролет/лято') | Q(collection__name='пролет/есен') | Q(collection__name='лято')
        items = items.filter(query)

        return items

    @property
    def meta_title(self):
        return 'Колекция пролет/лято - Онлайн Цени | Вили Стил'

    @property
    def meta_description(self):
        return ('Разгледайте предложенията за сезон пролет/лято на българския производител на дамски дрехи Вили Стил. '
                'За запитвания и поръчки - 0886531811')
