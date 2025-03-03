from django.urls import path, include

from fashionShop.accounts import views

urlpatterns = [
    path('', views.test, name='test'),
    path('login/', views.login, name='login')
]
