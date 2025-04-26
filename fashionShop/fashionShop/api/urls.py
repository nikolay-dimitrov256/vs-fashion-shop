from django.urls import path, include

from fashionShop.api import views

urlpatterns = [
    path('proxy/', include([
        path('speedy/', include([
            path('towns/', views.SpeedyTownsView.as_view(), name='speedy-towns'),
            path('offices/', views.SpeedyOfficeView.as_view(), name='speedy-offices'),
        ])),
        path('econt/', include([
            path('towns/', views.EcontTownsView.as_view(), name='econt-towns'),
            path('offices/', views.EcontOfficeView.as_view(), name='econt-offices'),
        ]))
    ]))
]
