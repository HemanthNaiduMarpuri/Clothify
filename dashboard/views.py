from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from .mixins import AdminRequiredMixin
from products.models import Product, Category, Brand
from accounts.models import Customer, DeliveryBoy
from django.db.models import Q
from orders.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ProductCreateForm, CategoryForm, BrandForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils.timezone import now
from complaints.models import Complaints

class DashboardView(generic.TemplateView):
    template_name = 'admin/admin_dashboard.html'
    today = timezone.localdate()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(OrderItem.objects.filter(status='paid'))
        context['total_orders'] = Order.objects.all().count()
        context['current_orders_count'] = Order.objects.filter(status='ongoing').count()
        context['completed_today'] = Order.objects.filter(status='delivered', created_at__date=self.today).count()
        context['total_revenue'] = OrderItem.objects.filter(status='paid').aggregate(total=Sum(ExpressionWrapper(F('price_at_order_time')*F('quantity'), output_field=DecimalField())))['total'] or 0
        context['total_users'] = Customer.objects.all().count()
        context['low_stock_items'] = Product.objects.filter(product_inventory__lte = 5).count()
        context['pending_returns'] = Order.objects.filter(status='cancelled').count()
        context['recent_orders'] = Order.objects.all().order_by('-created_at')[:10]
        return context

class AllProductsView(generic.ListView):
    model = Product
    template_name = 'admin/all_products.html'
    context_object_name = 'product'
    paginate_by = 20

    def get_queryset(self):
        qs = self.model.objects.all().select_related('category', 'brand')

        q = self.request.GET.get('q','').strip()
        brand_id = self.request.GET.get('brand', '').strip()

        if q:
            qs = qs.filter(Q(product_name__icontains=q) | Q(product_slug__icontains=q))
        if brand_id:
            qs = qs.filter(Q(brand_id=brand_id))
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['search_query'] = self.request.GET.get('q', '').strip()
        context['current_brand'] = self.request.GET.get('brand', '').strip()
        return context
    

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'admin/admin_product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = self.model.objects.filter(id=pk)
        return queryset

class AllCategoriesView(generic.ListView):
    model = Category
    template_name = 'admin/admin_categories.html'
    context_object_name = 'category'

    def get_queryset(self):
        qs = self.model.objects.all()

        q = self.request.GET.get('q', '').strip()

        if q:
            qs = qs.filter(Q(category_name__icontains = q) | Q(category_slug__icontains = q))
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '').strip()
        return context


class AllBrandsView(generic.ListView):
    model = Brand
    template_name = 'admin/admin_brands.html'
    context_object_name = 'brand'

    def get_queryset(self):
        qs = self.model.objects.all()

        q = self.request.GET.get('q', '').strip()

        if q:
            qs = qs.filter(Q(brand_name__icontains = q) | Q(brand_name__icontains = q))
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '').strip()
        return context

class AllCustomersView(generic.ListView):
    model = Customer
    template_name = 'admin/admin_customer.html'
    context_object_name = 'customers'
    paginate_by = 30
    
    def get_queryset(self):
        qs = self.model.objects.all()

        q = self.request.GET.get('sort', 'latest')
        if q == 'latest':
            qs = qs.order_by('join_date')
        elif q == 'oldest':
            qs = qs.order_by('-join_date')
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'latest').strip()
        return context
    
class AllDeliveryBoyView(generic.ListView):
    model = DeliveryBoy
    template_name = 'admin/admin_deliveryboy.html'
    context_object_name = 'deliveryboy'
    paginate_by = 30

    def get_queryset(self):
        qs = self.model.objects.filter(status='active')
        q = self.request.GET.get('sort', 'latest')

        if q == 'latest':
            qs = qs.order_by('join_date')
        elif q == 'oldest':
            qs = qs.order_by('-join_date')
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'latest')
        return context

class ProductStockView(generic.ListView):
    model = Product
    template_name = 'admin/admin_stock.html'    
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        stock_filter = self.request.GET.get('filter', 'all')

        if stock_filter == 'high':
            queryset = self.model.objects.filter(product_inventory__gte = 15)
        elif stock_filter == 'low':
            queryset = self.model.objects.filter(product_inventory__lt = 15)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context

class ApprovalView(generic.ListView):
    model = DeliveryBoy
    template_name = 'admin/approval.html'
    context_object_name = 'approval'

    def get_queryset(self):
        return self.model.objects.filter(status = 'inactive')
    
class AllOrdersView(generic.ListView):
    model = Order
    template_name = 'admin/all_orders.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

@require_POST
@login_required
def update_order_status(request, id):
    order = get_object_or_404(Order, id=id)
    status = request.POST.get('status')

    if status in dict(order.STATUS_CHOICES):
        order.status = status
        if status == 'delivered':
            order.delivered_at = now()
        order.save()

    return redirect('all_orders')

class PendingOrdersList(generic.ListView):
    model = Order
    template_name = 'admin/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(status='pending')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pending Orders'
        return context
    
class PaidOrdersList(generic.ListView):
    model = Order
    template_name = 'admin/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(status='paid')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Paid Orders'
        return context

class OngoingOrdersList(generic.ListView):
    model = Order
    template_name = 'admin/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(status='ongoing')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ongoing Orders'
        return context

class DeliveredOrdersList(generic.ListView):
    model = Order
    template_name = 'admin/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(status='delivered')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delivered Orders'
        return context
    
class RequestReturnedOrdersList(generic.ListView):
    model = Order
    template_name = 'admin/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(status='return_requested')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Return Requested Orders'
        return context

class CancelledOrdersList(generic.ListView):
    model = Order
    template_name = 'admin/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(status='cancelled')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cancelled Orders'
        return context

class PaymentsView(generic.ListView):
    model = Order
    template_name = 'admin/payments.html'
    context_object_name = 'payments'
    ordering = ['-created_at']

    def get_queryset(self):
        return OrderItem.objects.filter(status='paid')
    
@login_required    
def create_product(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created Successfully')
            return redirect('all_products')
    else:
        form = ProductCreateForm()
    
    context = {
        'form':form
    }

    return render(request, 'admin/product_create.html', context=context)

class UpdateProductView(generic.UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'admin/productupdate.html'
    context_object_name = 'product'

    slug_field = 'product_slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('all_products')

class BrandCreateView(generic.CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'admin/brandcreate.html'
    context_object_name = 'brand'

    def get_success_url(self):
        return reverse_lazy('all_brands')

class BrandUpdateView(generic.UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'admin/brandupdate.html'
    context_object_name = 'brand'

    slug_field = 'brand_slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('all_brands')

class CategoryCreateView(generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin/categorycreate.html'
    context_object_name = 'category'

    def get_success_url(self):
        return reverse_lazy('all_categories')

class CategoryUpdateView(generic.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin/categoryupdate.html'
    context_object_name = 'category'

    slug_field = 'category_slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('all_categories')
 
class ProductDeleteView(generic.DeleteView):
    model = Product
    template_name = 'admin/productdelete.html'
    context_object_name = 'product'

    slug_field = 'product_slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('all_products')

class CategoryDeleteView(generic.DeleteView):
    model = Category
    template_name = 'admin/categorydelete.html'
    context_object_name = 'category'

    slug_field = 'category_slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('all_categories')

class BrandDeleteView(generic.DeleteView):
    model = Brand
    template_name = 'admin/branddelete.html'
    context_object_name = 'brand'

    slug_field = 'brand_slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('all_brands')
    
class UserOrdersView(generic.ListView):
    model = Order
    template_name = 'admin/userorders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        customer = Customer.objects.get(id=user_id)
        orders = Order.objects.filter(customer=customer).order_by('-delivered_at')

        context['customer'] = customer
        context['orders'] = orders
        
        return context
    
@require_POST
def update_complaint_status(request, pk):
    complaint = get_object_or_404(Complaints, pk=pk)

    status = request.POST.get('status')
    if status in dict(complaint.STATUS_CHOICES):
        complaint.status = status
        complaint.save()

    return redirect('complaints')