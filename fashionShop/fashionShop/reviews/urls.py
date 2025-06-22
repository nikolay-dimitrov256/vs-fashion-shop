from django.urls import path

from fashionShop.reviews import views

urlpatterns = [
    path('create/<int:item_pk>/', views.submit_review, name='submit-review')
]