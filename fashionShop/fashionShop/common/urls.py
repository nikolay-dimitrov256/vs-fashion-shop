from django.urls import path

from fashionShop.common import views

urlpatterns = [
    path('', views.home, name='home'),
]
