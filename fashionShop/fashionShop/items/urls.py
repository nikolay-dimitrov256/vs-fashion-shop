from django.urls import path, include

from fashionShop.items import views

urlpatterns = [
    path('', views.ItemsListView.as_view(), name='all-items'),
    path('pants/', views.PantsListView.as_view(), name='pants'),
    path('skirts/', views.SkirtsListView.as_view(), name='skirts'),
    path('dresses/', views.DressesListView.as_view(), name='dresses'),
    path('shirts/', views.ShirtsListView.as_view(), name='shirts'),
    path('blouses/', views.BlousesListView.as_view(), name='blouses'),
    path('tunics/', views.TunicsListView.as_view(), name='tunics'),
    path('blazers/', views.BlazersListView.as_view(), name='blazers'),
    path('suits/', views.SuitsListView.as_view(), name='suits'),
    path('jackets/', views.JacketsListView.as_view(), name='jackets'),
    path('coats/', views.CoatsListView.as_view(), name='coats'),
    path('vests/', views.VestsListView.as_view(), name='vests'),
    path('cardigans/', views.CardigansListView.as_view(), name='cardigans'),
    path('underwear/', views.TankTopsListView.as_view(), name='underwear'),
    path('elegant/', views.ElegantListView.as_view(), name='elegant'),
    path('office/', views.OfficeListView.as_view(), name='office'),
    path('official/', views.OfficialListView.as_view(), name='official'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<slug:slug>/', include([
        path('', views.ItemDetailView.as_view(), name='item-details'),
    ]))
]
