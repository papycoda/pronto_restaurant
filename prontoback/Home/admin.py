from django.contrib import admin
from  .models import *
from django.db.models import F


# Register your models here.
admin.site.register(Category)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Reservation)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('name', 'price', 'category')
    ordering = [F('name').asc(nulls_last=True)]
