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
    ])),
    path('facebook/', views.products_feed, name='facebook-catalog'),
    path('items/', include([
        path('', views.ItemsListView.as_view(), name='api-items'),
        path('bestsellers/', views.BestsellersListView.as_view(), name='api-bestsellers'),
        path('new/', views.NewItemsListView.as_view(), name='api-new'),
        path('max/', views.MaxSizeListView.as_view(), name='api-max'),
        path('fall-winter/', views.FallWinterListView.as_view(), name='api-fall-winter'),
        path('spring-summer/', views.SpringSummerListView.as_view(), name='api-spring-summer'),
    ])),
]
