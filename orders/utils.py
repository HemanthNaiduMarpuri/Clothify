from decimal import Decimal
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce
from .models import Cart

def get_total_amount(customer):   
    return (
        Cart.objects
        .filter(customer=customer)
        .aggregate(
            total=Coalesce(
                Sum(ExpressionWrapper(F('product__product_price') * F('quantity'), output_field=DecimalField(max_digits=10, decimal_places=2))),
                Decimal('0.00')
            )
        )['total']
    )
