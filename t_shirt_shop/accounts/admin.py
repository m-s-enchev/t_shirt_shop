from django.contrib import admin

from t_shirt_shop.accounts.models import ShopUserModel

# Register your models here.


class UserAdminModel(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'last_login']
    search_fields = ['email', 'first_name', 'last_name']
    fields = ('email', 'is_active', 'first_name', 'last_name', 'last_login', 'date_joined')
    readonly_fields = ['last_login', 'date_joined']


admin.site.register(ShopUserModel, UserAdminModel)
