from django.urls import path

from t_shirt_shop.products import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products_all'),
    path('women/', views.ProductListViewWomen.as_view(), name='products_women'),
    path('men/', views.ProductListViewMen.as_view(), name='products_men'),
    path('kids/', views.ProductListViewKids.as_view(), name='products_kids'),
    path('<int:pk>/', views.product_single, name='product_single'),
]