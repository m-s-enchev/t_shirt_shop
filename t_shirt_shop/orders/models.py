from django.db import models

from t_shirt_shop.accounts.models import ShopUserModel, AnonymousUserData
from t_shirt_shop.products.models import Products
from t_shirt_shop.shopping_cart.models import ShoppingCart, ShoppingCartItems, AnonymousShoppingCart


# Create your models here.


class Orders(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ShopUserModel, on_delete=models.CASCADE, blank=True, null=True)
    anonymous_user_data = models.ForeignKey(AnonymousUserData, on_delete=models.SET_NULL, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Orders'

    def create_order_items_from_cart(self, session_key=None):
        cart_items = None

        if self.user and self.user.is_authenticated:
            cart_items = ShoppingCartItems.objects.filter(cart__user=self.user)
        elif session_key:
            try:
                anonymous_user_data = AnonymousUserData.objects.get(session_key=session_key)
                self.anonymous_user_data = anonymous_user_data
                anonymous_cart = AnonymousShoppingCart.objects.get(session_key=session_key)
                cart_items = ShoppingCartItems.objects.filter(cart=anonymous_cart.cart)
            except AnonymousUserData.DoesNotExist:
                raise ValueError("Session key is required for anonymous users")
        else:
            raise ValueError("Session key is required for anonymous users")

        for item in cart_items:
            OrdersItems.objects.create(order=self, product=item.product, quantity=item.quantity)

        if not self.user or not self.user.is_authenticated:
            cart_items.delete()
    inlines = ['OrdersItems']


class OrdersItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Orders Items'

    def total_price(self):
        return self.product.price * self.quantity

