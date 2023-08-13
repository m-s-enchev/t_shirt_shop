from django.contrib import admin

from t_shirt_shop.orders.models import OrdersItems, Orders


# Register your models here.

class OrdersItemsAdmin(admin.TabularInline):
    model = OrdersItems
    fields = ('product', 'quantity', 'price')


class OrdersAdmin(admin.ModelAdmin):
    fields = ['date_created', 'email', 'first_name', 'last_name', 'is_completed', 'is_canceled']
    list_display = ('id', 'date_created', 'email', 'first_name', 'last_name', 'is_completed', 'is_canceled')
    readonly_fields = ['date_created']
    search_fields = ['email', 'first_name', 'last_name']

    inlines = [OrdersItemsAdmin]


admin.site.register(Orders, OrdersAdmin)

