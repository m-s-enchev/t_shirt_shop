from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from t_shirt_shop.accounts.models import ShopUserModel, UserProfileModel, MyDesignsModel


# Register your models here.

class ProfileAdmin(admin.TabularInline):
    model = UserProfileModel
    fields = ['phone_number', 'address']


class ShopUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'last_login']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['last_login', 'date_joined']
    ordering = ("email",)
    inlines = [ProfileAdmin]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.register(ShopUserModel, ShopUserAdmin)
admin.site.register(MyDesignsModel)
