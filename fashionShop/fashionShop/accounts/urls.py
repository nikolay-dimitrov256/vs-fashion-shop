from django.contrib.auth.views import LogoutView
from django.urls import path, include

from fashionShop.accounts import views

urlpatterns = [
    path('', views.test, name='test'),
    path('login/', views.AppUserLoginView.as_view(), name='login'),
    path('register/', views.AppUserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
]
