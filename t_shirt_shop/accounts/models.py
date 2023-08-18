from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from t_shirt_shop.accounts.validators import phone_number_validator


class UserProfileModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, validators=[phone_number_validator])


class ShopUserModel(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,
                                  validators=[MinLengthValidator(2)]
                                  )
    last_name = models.CharField(max_length=30,
                                 validators=[MinLengthValidator(2)]
                                 )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class AnonymousUserData(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=False)
    first_name = models.CharField(max_length=30,
                                  validators=[MinLengthValidator(2)]
                                  )
    last_name = models.CharField(max_length=30,
                                 validators=[MinLengthValidator(2)]
                                 )
    phone_number = models.CharField(max_length=10, validators=[phone_number_validator])
    address = models.CharField(max_length=100)


class MyDesignsModel(models.Model):
    user = models.ForeignKey(ShopUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='custom_user_designs/')

    class Meta:
        verbose_name_plural = 'Custom user designs'

    def __str__(self):
        return self.name



