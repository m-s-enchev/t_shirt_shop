from django.contrib import admin

from t_shirt_shop.products.models import Products, Categories

# Register your models here.


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']


admin.site.register(Products, ProductsAdmin)
admin.site.register(Categories)
