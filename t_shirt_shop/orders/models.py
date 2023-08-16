from django.db import models

from t_shirt_shop.accounts.models import ShopUserModel, AnonymousUserData, UserProfileModel
from t_shirt_shop.products.models import Products
from t_shirt_shop.shopping_cart.models import ShoppingCart, ShoppingCartItems, AnonymousShoppingCart


# Create your models here.


class Orders(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    user = models.ForeignKey(ShopUserModel, on_delete=models.CASCADE, blank=True, null=True)
    anonymous_user_data = models.ForeignKey(AnonymousUserData, on_delete=models.SET_NULL, blank=True, null=True)

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
            OrdersItems.objects.create(order=self, product=item.product, quantity=item.quantity, price=item.price)

        if not self.user or not self.user.is_authenticated:
            cart_items.delete()

    def save(self, *args, **kwargs):
        if self.user and self.user.is_authenticated:
            profile = UserProfileModel.objects.get(user=self.user)
            self.email = self.user.email
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
            self.address = profile.address
            self.phone_number = profile.phone_number
        elif self.anonymous_user_data:
            self.email = self.anonymous_user_data.email
            self.first_name = self.anonymous_user_data.first_name
            self.last_name = self.anonymous_user_data.last_name

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id}"


class OrdersItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=5)

    class Meta:
        verbose_name_plural = 'Orders Items'

    def total_price(self):
        return self.product.price * self.quantity

