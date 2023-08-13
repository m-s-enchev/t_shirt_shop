from django.contrib import admin

from t_shirt_shop.contact_form_messages.models import MessagesModel


# Register your models here.


class MessagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['email', 'name']
    fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'message']


admin.site.register(MessagesModel, MessagesAdmin)
