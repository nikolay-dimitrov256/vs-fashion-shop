from django.urls import path

from fashionShop.common import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('single/', views.SingleView.as_view(), name='single'),
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
