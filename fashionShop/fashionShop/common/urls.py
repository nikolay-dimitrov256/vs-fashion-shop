from django.urls import path

from fashionShop.common import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('single/', views.SingleView.as_view(), name='single'),
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact-message/', views.ContactMessageView.as_view(), name='contact-message'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('our-shops', views.OurShopsView.as_view(), name='our-shops'),
    path('shopping-terms', views.ShoppingTermsView.as_view(), name='shopping-terms'),
    path('shipping-terms/', views.ShippingTermsView.as_view(), name='shipping-terms'),
    path('refunds/', views.RefundsView.as_view(), name='refunds'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    # path('set-currency/', views.set_currency, name='set-currency')
]
