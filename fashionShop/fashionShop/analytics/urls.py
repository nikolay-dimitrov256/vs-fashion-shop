from django.urls import path

from fashionShop.analytics import views

urlpatterns = [
    path('sales-by-size/', views.SalesBySizeView.as_view(), name='sizes-sales')
]