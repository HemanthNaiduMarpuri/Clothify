from django.contrib import admin
from .models import Favoriates, Cart, Order, OrderItem

admin.site.register(Favoriates)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
