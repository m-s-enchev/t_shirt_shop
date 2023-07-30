from django.contrib import admin

from t_shirt_shop.products.models import Product, Category

# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
