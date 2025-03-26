from django.urls import path, include

from fashionShop.items import views

urlpatterns = [
    path('<int:pk>/', include([
        path('', views.ItemDetailView.as_view(), name='item-details'),
    ]))
]
