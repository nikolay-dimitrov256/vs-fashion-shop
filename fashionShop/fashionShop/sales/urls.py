from django.urls import path, include

from fashionShop.sales import views

urlpatterns = [
    path('cart/', include([
        path('<int:pk>', include([
            path('add/', views.add_to_cart, name='add-to-cart'),
            ])),
        ]),
    ),
]
