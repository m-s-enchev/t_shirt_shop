from django.db import models

from t_shirt_shop.accounts.models import ShopUserModel
from t_shirt_shop.products.models import Products


# Create your models here.

class AnonymousShoppingCart(models.Model):
    cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)


class ShoppingCart(models.Model):
    user = models.ForeignKey(ShopUserModel, on_delete=models.CASCADE, null=True, blank=True)
    session_carts = models.ManyToManyField(AnonymousShoppingCart, related_name='shopping_carts', blank=True)


class ShoppingCartItems(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=5)

    def total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        if self.product:
            self.price = self.product.price
        super().save(*args, **kwargs)

