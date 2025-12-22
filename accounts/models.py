from django.db import models
from django.contrib.auth.models import AbstractUser

STATUS_CHOICES = [
    ('active', 'active'),
    ('inactive', 'inactive')
]

ACCOUNT_CHOICES = [
    ('customer', 'customer'),
    ('delivery boy', 'delivery boy'),
    ('admin', 'admin')
]


class Register(AbstractUser):
    user_role = models.CharField(max_length=20, choices=ACCOUNT_CHOICES, default='customer')

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name="register_user_set", 
        related_query_name="register_user",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name="register_user_permissions_set", 
        related_query_name="register_user",
    )

    def __str__(self):
        return f"{self.username} ({self.user_role})"


class Customer(models.Model):
    user = models.OneToOneField(Register, on_delete=models.CASCADE, related_name='customer_profile')
    image = models.ImageField(upload_to='user_profile_images/', blank=True, null=True)
    contact = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.user.username


class DeliveryBoy(models.Model):
    user = models.OneToOneField(Register, on_delete=models.CASCADE, related_name='delivery_profile')
    image = models.ImageField(upload_to='deliveryboy_profile_images/', blank=True, null=True)
    contact = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    idproof = models.CharField(max_length=50, blank=True, null=True)
    idproof_image = models.ImageField(upload_to='idproof_images/', blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.user.username
