from django.urls import path, include

from fashionShop.api import views

urlpatterns = [
    path('proxy/', include([
        path('speedy/', include([
            path('towns/', views.SpeedyTownsView.as_view(), name='speedy-towns'),
            path('office/', views.SpeedyOfficeView.as_view(), name='speedy-office'),
        ]))
    ]))
]
