from django.db import models
from products.models import Product
from accounts.models import Customer
from datetime import timedelta
from django.utils.timezone import now

class Favoriates(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='favoriates')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favoriated_by')

    class Meta:
        unique_together = ('customer', 'product')
    
    def __str__(self):
        return f"{self.customer} -> {self.product}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='added_by')
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('customer', 'product')
    
    def __str__(self):
        return f"{self.customer} -> {self.product}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('return_requested', 'return_requested'),
        ('cancelled', 'cancelled'),
        ('ongoing', 'ongoing'),
        ('delivered', 'delivered')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    recipient_name = models.CharField(max_length=255, blank=True, null=True)
    recipient_phone = models.CharField(max_length=30, blank=True, null=True)
    address_text = models.TextField(blank=True, null=True)

    latitude = models.DecimalField(max_digits=15, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=8, blank=True, null=True)

    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    def is_return_eligible(self):
        if self.status != 'delivered' or not self.delivered_at:
            return False
        return now() <= self.delivered_at + timedelta(days=4)

    def __str__(self):
        return f"Order{self.id} - {self.customer} -> {self.status}"
    
class OrderItem(models.Model):
    STATUS_CHOICES = (
        ('paid', 'paid'),
        ('pending', 'pending')
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def sub_total(self):
        return self.quantity * self.price_at_order_time
    
    def __str__(self):
        return f"{self.product} * {self.quantity} (Order-{self.order.id})"