from django.contrib import admin
from  .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(DrinkItem)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Reservation)
