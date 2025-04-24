from django.urls import path, include

from fashionShop.sales import views

urlpatterns = [
    path('cart/', include([
        path('', views.view_cart_view, name='view-cart'),
        path('clear/', views.clear_cart_view, name='clear-cart'),
        path('<int:pk>/', include([
            path('add/', views.add_to_cart, name='add-to-cart'),
            path('remove/', views.remove_from_cart_view, name='remove-from-cart'),
            ])),
        ]),
    ),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('phone-order/', views.PhoneOrderView.as_view(), name='phone-order'),
    path('shipping-order/', views.ShippingOrderView.as_view(), name='shipping-order'),
    path('order/<int:pk>/', views.ThankYouView.as_view(), name='order'),
]
