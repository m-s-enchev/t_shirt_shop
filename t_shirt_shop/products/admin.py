from django.contrib import admin

from t_shirt_shop.products.models import Products, Categories

# Register your models here.


admin.site.register(Products)
admin.site.register(Categories)
