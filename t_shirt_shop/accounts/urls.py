from django.urls import path

from t_shirt_shop.accounts import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('view/', views.user_details_view, name='user_details_view'),
    path('my-designs/', views.my_designs, name='my_designs')
]