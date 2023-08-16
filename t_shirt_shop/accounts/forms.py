from django.contrib.auth.forms import BaseUserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

from t_shirt_shop.accounts.models import ShopUserModel, UserProfileModel, AnonymousUserData, MyDesignsModel


class ShopUserRegistrationForm(BaseUserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "At least 8 characters long"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat password"}),
        strip=False,
    )

    class Meta:
        model = ShopUserModel
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Valid email for login and order information'}),
        }


class ShopUserLoginForm(AuthenticationForm):
    pass


class ViewUserInfo(forms.ModelForm):
    class Meta:
        model = ShopUserModel
        fields = ['first_name', 'last_name', 'email']


class ViewProfileInfo(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = ['phone_number', 'address']


class ViewAnonymousUserInfo(forms.ModelForm):
    class Meta:
        model = AnonymousUserData
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']


class AddCustomDesigns(forms.ModelForm):
    class Meta:
        model = MyDesignsModel
        fields = ['name', 'image']
