from django.http import HttpResponse
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import xml.dom.minidom

from django.urls import reverse_lazy

from fashionShop.items.models import Item


def products_feed(request):
    rss = Element("rss", {
        "version": "2.0",
        "xmlns:g": "http://base.google.com/ns/1.0",
        "xmlns:atom": "http://www.w3.org/2005/Atom"
    })
    channel = SubElement(rss, 'channel')
    SubElement(channel, 'title').text = 'Vili Style catalog'
    SubElement(channel, 'description').text = 'Vili Style product feed for Facebook'
    SubElement(channel, 'link').text = request.build_absolute_uri(reverse_lazy('home'))
    SubElement(channel, 'atom:link', {
        'href': request.build_absolute_uri(reverse_lazy('facebook-catalog')),
        'rel': 'self',
        'type': 'application/rss+xml'
    })

    items = (
        Item.objects
        .exclude(deleted=True)
        .prefetch_related(
            'pictures',
            'style',
            'order_items',
        )
        .select_related(
            'category',
            'color_group',
            'collection'
        )
    )

    for item in items:
        it = SubElement(channel, 'item')
        SubElement(it, 'g:id').text = str(item.pk)
        SubElement(it, 'g:title').text = item.name_bg
        SubElement(it, 'g:description').text = item.description_bg
        SubElement(it, 'g:link').text = request.build_absolute_uri(reverse_lazy('item-details', kwargs={'slug': item.slug}))
        SubElement(it, 'g:image_link').text = item.pictures.first().image_url if item.pictures.first() else ''
        SubElement(it, 'g:availability').text = 'in stock'
        SubElement(it, 'g:condition').text = 'new'
        SubElement(it, 'g:price').text = f'{item.price} BGN'
        SubElement(it, 'g:sale_price').text = f'{item.discount_price} BGN'
        SubElement(it, 'g:brand').text = 'Вили Стил'
        SubElement(it, 'color').text = item.color_group.name_bg if item.color_group else ''
        SubElement(it, 'g:google_product_category').text = item.category.name_bg

        if len(item.pictures.all()) > 1:
            SubElement(it, 'additional_image_link').text = item.pictures.all()[1].image_url
        if len(item.pictures.all()) > 2:
            SubElement(it, 'additional_image_link').text = item.pictures.all()[2].image_url

        for style in item.style.all():
            SubElement(it, 'style').text = style.name

        sales = item.order_items.count()

        SubElement(it, 'custom_label_1').text = str(item.is_new)
        SubElement(it, 'custom_label_2').text = str(sales >= 5)
        SubElement(it, 'custom_label_3').text = item.collection.name if item.collection else ''

    xml_str = tostring(rss, encoding='utf-8')
    # pretty_xml = xml.dom.minidom.parseString(xml_str).toprettyxml(indent='  ')

    return HttpResponse(xml_str, content_type='application/xml')
