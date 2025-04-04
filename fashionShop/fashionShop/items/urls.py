from django.urls import path, include

from fashionShop.items import views

urlpatterns = [
    path('', views.ItemsListView.as_view(), name='all-items'),
    path('<slug:slug>/', include([
        path('', views.ItemDetailView.as_view(), name='item-details'),
    ]))
]
