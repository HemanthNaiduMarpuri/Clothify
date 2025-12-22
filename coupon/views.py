from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from accounts.models import Customer
from orders.utils import get_total_amount
from .models import Coupon, CouponUsage

@login_required
def apply_coupon(request):
    if request.method != 'POST':
        return redirect('cart_list')

    coupon_code = request.POST.get('coupon')
    if not coupon_code:
        messages.error(request, "Invalid Coupon Code")
        return redirect('cart_list')
    
    try:
        coupon = Coupon.objects.get(coupon__iexact=coupon_code)
    except Coupon.DoesNotExist:
        messages.error(request, 'Coupon Does not Exist')
        return redirect('cart_list')
    
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found")
        return redirect('cart_list')
    cart_total = get_total_amount(customer)
    if not coupon.is_valid(cart_total):
        messages.error(request, "Minimum Cart Total is Required for this copoun")
        return redirect('cart_list')
    
    if CouponUsage.objects.filter(customer=customer, coupon=coupon).exists():
        messages.error(request, "This Coupon is already is used.")
        return redirect('cart_list')
    
    request.session['coupon_id'] = coupon.id
    messages.success(request, "Cart Applied Successfully")
    return redirect('cart_list')

@login_required
def remove_coupon(request):
    request.session.pop('coupon_id', None)
    messages.success(request, "Coupon Removed Successfully")
    return redirect('cart_list')