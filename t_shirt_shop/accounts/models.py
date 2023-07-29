from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class ShopUserModel(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,
                                  validators=[MinLengthValidator(5)]
                                  )
    last_name = models.CharField(max_length=30,
                                 validators=[MinLengthValidator(5)]
                                 )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




