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
]
