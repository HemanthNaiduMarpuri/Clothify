from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Register, Customer, DeliveryBoy
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def create_user_profile(sender, user, **kwargs):
    Customer.objects.create(user=user)
        
        
