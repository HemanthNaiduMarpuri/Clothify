from django.db import models
from accounts.models import Customer

class Coupon(models.Model):
    COUPON_CHOICES = (
        ('percentage', 'percentage'),
        ('flat', 'flat')
    )

    coupon = models.CharField(max_length=30, unique=True)
    coupon_type = models.CharField(max_length=30, choices=COUPON_CHOICES)
    coupon_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_amount_for_coupon = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.coupon = self.coupon.upper()
        super().save(*args, **kwargs)

    def is_valid(self, cart_total):
        from django.utils import timezone
        now = timezone.now()

        return(self.is_active and self.valid_from <= now <= self.valid_to and self.min_amount_for_coupon <= cart_total)
    
    def __str__(self):
        return f"{self.coupon} -> {self.coupon_type} -> {self.coupon_value}"
    
class CouponUsage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'coupon')

    def __str__(self):
        return f"{self.customer} -> {self.coupon}"