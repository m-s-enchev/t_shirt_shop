from django.urls import path

from t_shirt_shop.shopping_cart import views

urlpatterns = [
    path('', views.shopping_cart_view, name='view_cart'),
    path('add-to-cart/<int:pk>', views.add_to_shopping_cart, name='add_to_shopping_cart'),
    path('shipping-details/', views.shipping_details_view, name='shipping_details')
]
