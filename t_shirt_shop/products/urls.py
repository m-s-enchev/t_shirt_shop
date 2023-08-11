from django.urls import path

from t_shirt_shop.products import views

urlpatterns = [
    path('', views.products_all, name='products_all'),
    path('<int:pk>/', views.product_single, name='product_single'),
]