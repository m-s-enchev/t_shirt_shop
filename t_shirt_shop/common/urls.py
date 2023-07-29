from django.urls import path

from t_shirt_shop.common import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
]