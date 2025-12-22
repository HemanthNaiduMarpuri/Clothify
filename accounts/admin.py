from django.contrib import admin
from .models import Customer, Register, DeliveryBoy

admin.site.register(Register)
admin.site.register(Customer)
admin.site.register(DeliveryBoy)
