from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from t_shirt_shop.accounts.forms import ShopUserRegistrationForm, ShopUserLoginForm
from t_shirt_shop.accounts.models import ShopUserModel


# Create your views here.

class UserRegisterView(generic.CreateView):
    model = ShopUserModel
    form_class = ShopUserRegistrationForm
    template_name = 'accounts/user-register.html'
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    template_name = 'accounts/user-login.html'
    form_class = ShopUserLoginForm
    next_page = reverse_lazy('homepage')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('homepage')
