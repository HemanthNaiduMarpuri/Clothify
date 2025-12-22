from django.db import models
from accounts.models import Customer

class Complaints(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('in-progress', 'in-progess'),
        ('resolved', 'resolved'),
        ('rejected', 'rejected')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='complaints')
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    complaint_msg = models.TextField()
    status = models.CharField(max_length=20 ,choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} -> {self.full_name} -> {self.email}"

class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='subscription')
    email = models.CharField(max_length=255)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} -> {self.email}"