from django.http import JsonResponse
from django.views import generic
from products.models import Category, Product, Brand
from django.db.models import Q
from accounts.models import Customer
from orders.models import Cart
from django.contrib import messages
from complaints.models import Subscription
from django.shortcuts import get_object_or_404

class HomepageView(generic.TemplateView):
    template_name = 'homepage.html'

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Please enter an email address.")
            return self.get(request, *args, **kwargs)
        
        if Subscription.objects.filter(customer=customer).exists():
            messages.info(request, "Customer Already Subscribed!")
        else:
            Subscription.objects.get_or_create(customer=customer, email=email)
            messages.success(request, "Thanks for subscribing!")
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        recently_added = Product.objects.all().order_by('-uploaded_at')[:15]
        discounted = Product.objects.filter(has_discounted=True).order_by('uploaded_at')[:20]
        categories = Category.objects.all()
        brands = Brand.objects.all()

        user = self.request.user

        if user.is_authenticated:
            try:
                customer = Customer.objects.get(user=user)
                cart_items = Cart.objects.filter(customer=customer)

                cart_map = {item.product_id: item.quantity for item in cart_items}

                for p in recently_added:
                    p.cart_quantity = cart_map.get(p.id, 0)

                for p in discounted:
                    p.cart_quantity = cart_map.get(p.id, 0)

            except Customer.DoesNotExist:
                pass

        context['recently_added_products'] = recently_added
        context['discounted_products'] = discounted
        context['categories'] = categories
        context['brands'] = brands

        return context
    

class AboutUsView(generic.TemplateView):
    template_name = 'aboutus.html'

def search_view(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(product_slug__icontains = query)).order_by('uploaded_at')[:10]
        data = [
            {'name':p.product_name, 'slug':p.product_slug}
            for p in products
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

class CategoryListView(generic.ListView):
    model = Category
    template_name = 'products/categories_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()