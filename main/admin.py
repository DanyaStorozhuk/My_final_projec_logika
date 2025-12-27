from django.contrib import admin
from .models import CustomUser, Menu, Restaurant, Order, Workers, Comments 
# Register your models here.

admin.site.register(Workers)
admin.site.register(CustomUser)
admin.site.register(Menu)
admin.site.register(Comments)
admin.site.register(Restaurant)
admin.site.register(Order)