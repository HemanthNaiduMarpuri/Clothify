from decimal import Decimal
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.views import View, generic
from django.shortcuts import get_object_or_404, redirect, render
from .models import Favoriates, Cart, Order, OrderItem
from products.models import Product
from accounts.models import Customer
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import stripe
from django.conf import settings
from .forms import CheckOutForm
import simplejson as json
from coupon.models import Coupon, CouponUsage
from .utils import get_total_amount

stripe.api_key = settings.STRIPE_SECRET_KEY

class FavoriteView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('account_login')
        
        customer = Customer.objects.get(user=request.user)
        product = get_object_or_404(Product, pk=pk)
        

        favoriate, created = Favoriates.objects.get_or_create(
            product = product, 
            customer = customer
        )

        if created:
            is_favoriated = True
        else:
            favoriate.delete()
            is_favoriated = False

        favorite_count = Favoriates.objects.filter(product=product).count()

        return JsonResponse({
            'authenticate':True,
            'is_favoriated':is_favoriated,
            'favorite_count':favorite_count
        })
    
class FavoriteListView(generic.ListView):
    model = Favoriates
    template_name = 'orders/favorite_list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Favoriates.objects.filter(customer=customer).select_related('product')
    
class CartView(View):
    def post(self,request,pk):
        if not request.user.is_authenticated:
            return redirect('account_login')
    
        product = get_object_or_404(Product, pk=pk)
        customer = Customer.objects.get(user=request.user)

        cart, created = Cart.objects.get_or_create(
            customer=customer,
            product=product,
            defaults={'quantity':1}
        )

        if created:
            return redirect('cart_list')
        else:
            action = request.POST.get('action', '').strip()
            if action == 'decrease':
                if cart.quantity == 1:
                    cart.delete()
                    return redirect('cart_list')
                else:
                    cart.quantity -= 1
                    cart.save()
            else:
                cart.quantity += 1
                cart.save()

        return redirect('cart_list')

@login_required
def cart_view(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        cart_items = Cart.objects.none()
        cart_total = Decimal('0.00')
        coupon = None
        discount = Decimal('0.00')
        final_total = cart_total
        delivery_fee = Decimal('0.00') 
    else:
        cart_items = Cart.objects.filter(customer=customer).select_related('product')

        cart_total = Decimal('0.00')
        for item in cart_items:
            product = item.product
            if hasattr(product, 'discounted_price') and product.has_discounted:
                price = product.discounted_price
            else:
                price = product.product_price
            
            cart_total += item.quantity * price
        coupon = None
        discount = Decimal('0.00')
        final_total = cart_total

        if cart_total >= Decimal('199'):
            delivery_fee = Decimal('0')
        else:
            delivery_fee = Decimal('29')

        coupon_id = request.session.get('coupon_id')
        if coupon_id:
            coupon = Coupon.objects.get(id=coupon_id)
            if coupon.coupon_type == 'percentage':
                discount = (cart_total * coupon.coupon_value)/100
            else:
                discount = coupon.coupon_value
        discount = min(discount, cart_total)
        final_total = (cart_total - discount) + delivery_fee
            
    context = {
        'cart_items' : cart_items,
        'cart_total' : cart_total,
        'discount' : discount,
        'final_total' : final_total,
        'coupon' : coupon,
        'delivery_fee' : delivery_fee
    }
    return render(request, 'orders/cart.html', context)

@login_required
def check_details_view(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Exception:
        customer = None

    session_data = request.session.get('checkout_data', {})
    initial = {
        'recipient_name':session_data.get('recipient_name') or (getattr(customer, 'fullname', '') if customer else '') or request.user.get_full_name(),
        'recipient_phone':session_data.get('recipient_phone') or (getattr(customer, 'phone', '') if customer else ''),
        'address_text':session_data.get('address_text') or (getattr(customer, 'address', '') if customer else ''),
        'latitude':session_data.get('latitude') or None,
        'longitude':session_data.get('longitude') or None,
    }

    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            request.session['checkout_data'] = {
                'recipient_name' : form.cleaned_data['recipient_name'],
                'recipient_phone' : form.cleaned_data['recipient_phone'],
                'address_text' : form.cleaned_data['address_text'],
                'latitude' : json.dumps(form.cleaned_data.get('latitude') or None),
                'longitude' : json.dumps(form.cleaned_data.get('longitude') or None),
            }
            request.session.modified = True

            return redirect('create_checkout_session')
    else:
        form = CheckOutForm(initial=initial)
  
    cart_items = Cart.objects.filter(customer=customer).select_related('product')
    subtotal = Decimal('0')

    for item in cart_items:
        price = item.product.product_price or item.product.discounted_price
        subtotal += price * item.quantity

    deivery_fee = Decimal('0') if subtotal > Decimal('199') else Decimal('29')
    grand_total = subtotal + deivery_fee

    context={
        'form':form,
        'cart_items':cart_items,
        'data':request.session.get('checkout_data')
    }

    return render(request, 'orders/post_to_checkout.html', context)

@login_required
def create_checkout_session(request):
    customer = Customer.objects.get(user=request.user)
    cart_items = Cart.objects.filter(customer=customer).select_related('product')

    if not cart_items.exists():
        return redirect('homepage')
    
    checkout_data = request.session.get('checkout_data')
    if not checkout_data:
        return redirect('check_details')
    
    final_total = get_total_amount(customer)
    
    Delivery_fee = Decimal('29')

    coupon_id = request.session.get('coupon_id', None)
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            if coupon.is_valid(final_total):
                if coupon.coupon_type == 'percentage':
                    discount = (final_total * coupon.coupon_value)/100
                else:
                    discount = coupon.coupon_value
                discount = min(discount, final_total)
        except Coupon.DoesNotExist:
            pass

        final_total -= discount
    
    line_items = []

    line_items.append({
        "price_data":{
            "currency":"inr",
            "product_data":{
                "name":"Total Bill -- Clothify(without delivery fee)",
            },
            'unit_amount':int(final_total * 100)
        },
        "quantity":1
    })

    if final_total >= Decimal('199'):
        Delivery_fee = Decimal('0')
    else:
        final_total += Delivery_fee

        line_items.append({
            "price_data":{
                "currency":"inr",
                "product_data":{
                    "name":"Delivery Fee",
                },
                "unit_amount":int(Delivery_fee * 100),
            },
            "quantity":1
        })
    
    if final_total < Decimal('50'):
        return redirect('cart_list')
    
    order = Order.objects.create(
        customer=customer, 
        status='pending', 
        total_amount=final_total,
        delivery_fee=Delivery_fee,
        recipient_name=checkout_data.get('recipient_name'),
        recipient_phone=checkout_data.get('recipient_phone'),
        address_text=checkout_data.get('address_text'),
        latitude=checkout_data.get('latitude') or None,
        longitude=checkout_data.get('longitude') or None,
    )

    for items in cart_items:
        price = items.product.product_price or items.product.discounted_price

        order_item = OrderItem.objects.create(order=order, product=items.product, quantity=items.quantity, price_at_order_time=price)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode = 'payment',
            line_items=line_items,
            success_url = request.build_absolute_uri(reverse('success'))+ "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = request.build_absolute_uri(reverse('cancel'))+ "?session_id={CHECKOUT_SESSION_ID}"
        )
    except Exception as e:
        order.delete()
        return redirect('cart_list')
    order.stripe_session_id = session.id
    order.save()

    return redirect(session.url)

@login_required
def stripe_success(request):
    session_id = request.GET.get('session_id')
    order = get_object_or_404(Order, stripe_session_id=session_id)
    customer = Customer.objects.get(user=request.user)

    coupon_id = request.session.get('coupon_id', None)
    try:
        if coupon_id:
            coupon = Coupon.objects.get(id=coupon_id)
            CouponUsage.objects.create(customer=customer ,coupon=coupon)
    except Coupon.DoesNotExist:
        pass
    
    order.status = 'paid'
    order.save()

    order_item = OrderItem.objects.filter(order=order)
    order_item.update(status='paid')

    for item in order_item:
        product = item.product
        product.product_inventory -= item.quantity
        product.save()

    Cart.objects.filter(customer=order.customer).delete()
    
    request.session.pop('checkout_data', None)
    request.session.pop('coupon_id', None)

    return render(request, 'orders/success_url.html', context={'order':order})

@login_required
def stripe_cancel(request):
    session_id = request.GET.get('session_id')
    order = get_object_or_404(Order, stripe_session_id=session_id)
    
    order.status = 'pending'
    order.save()

    OrderItem.objects.filter(order=order).update(status='pending')

    return render(request, 'orders/cancel_url.html', context={})

class OrdersList(generic.ListView):
    model = Order
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = Order.objects.filter(customer__user=self.request.user)

        status = self.request.GET.get('status', 'paid')

        if status in ['paid', 'cancelled', 'pending', 'delivered', 'ongoing']:
            qs = qs.filter(status=status)
        
        return qs
    
@login_required
def request_return(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if not order.is_return_eligible:
        return HttpResponseForbidden("Return Window Closed")
    
    order.status = 'return_requested'
    order.save()

    return redirect('orders_list')
    
    