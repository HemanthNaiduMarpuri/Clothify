from django.shortcuts import render
from django.views import generic
from .models import Category, Product, Brand
from orders.models import Favoriates, Cart, OrderItem
from accounts.models import Customer
from comments.models import Comment
from comments.forms import CommentForm

class ProductsListView(generic.ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    paginate_by = 21

    def get_queryset(self):
        queryset = Product.objects.filter(has_discounted=False)

        q = self.request.GET.get('q')
        brand = self.request.GET.get('brand')
        category = self.request.GET.get('category')
        min_price = self.request.GET.get('min_pice')
        max_price = self.request.GET.get('max_price')
        discount = self.request.GET.get('discount')

        if q:
            queryset = queryset.filter(product_name__icontains = q)

        if brand:
            queryset = queryset.filter(brand__brand_slug = brand)

        if category:
            queryset = queryset.filter(category__category_slug = category)
        
        if min_price:
            queryset = queryset.filter(product_price__gte = min_price)
        
        if max_price:
            queryset = queryset.filter(product_price__lte = max_price)
        
        if discount == '1':
            queryset = queryset.filter(has_discounted = True)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        return context
    
class DiscountedProductsListView(generic.ListView):
    model = Product
    template_name = 'products/discounted_products_list.html'
    context_object_name = 'discount'

    def get_queryset(self):
        queryset = Product.objects.filter(has_discounted=True)
        q = self.request.GET.get('q')
        brand = self.request.GET.get('brand')
        category = self.request.GET.get('category')
        min_price = self.request.GET.get('min_pice')
        max_price = self.request.GET.get('max_price')

        if q:
            queryset = queryset.filter(product_name__icontains = q)

        if brand:
            queryset = queryset.filter(brand__brand_slug = brand)
        
        if category:
            queryset = queryset.filter(category__category_slug = category)

        if min_price:
            queryset = queryset.filter(product_price__gte = min_price)
        
        if max_price:
            queryset = queryset.filter(product_price__lte = max_price)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product_detail'
    RELATED_PRODUCT_COUNT = 25

    slug_field = 'product_slug'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_product = self.object
        context['is_available_for_buy'] = current_product.product_inventory > 0
        related_products = Product.objects.filter(category=current_product.category).exclude(pk=current_product.pk).order_by('?')[:self.RELATED_PRODUCT_COUNT]
        related_products_count = related_products.count()
        is_favorited = False
        user = self.request.user

        if user.is_authenticated and hasattr(user, 'customer'):
            is_favorited = Favoriates.objects.filter(
                product = current_product,
                customer = user
            ).exists()
        
        quantity = 0
        if user.is_authenticated:
            try:
                customer = Customer.objects.get(user=self.request.user)
                cart = Cart.objects.filter(customer=customer ,product=current_product).first()
                if cart:
                    quantity = cart.quantity
            except Customer.DoesNotExist:
                pass
            
        context['quantity_in_cart'] = quantity
        favorite_count = Favoriates.objects.filter(product=current_product).count()

        if related_products_count < self.RELATED_PRODUCT_COUNT:
            filler_count = self.RELATED_PRODUCT_COUNT - related_products_count
            exclude_product_pks = list(related_products.values_list('pk', flat=True))
            exclude_product_pks.append(current_product.pk)
            random_products = Product.objects.exclude(pk__in=exclude_product_pks).order_by('?')[:filler_count]
            final_recommended_products = list(related_products) + list(random_products)
        else:
            final_recommended_products = list(related_products)
        
        comments = Comment.objects.all().order_by('-created_at')[:5]
        
        if self.request.user.is_authenticated:
            customer = Customer.objects.get(user=self.request.user)
            has_purchased = OrderItem.objects.filter(
                order__customer = customer,
                order__status = 'delivered',
                product = current_product
            ).exists()
            context['has_purchased'] = has_purchased
        if current_product.has_discounted:
            discount_percent = ((current_product.original_price - current_product.discounted_price)/(current_product.original_price)) * 100
            print(discount_percent)
        else:
            discount_percent = 0
        context['recommended_products'] = final_recommended_products
        context['is_favorited'] = is_favorited
        context['favorite_count'] = favorite_count
        context['comments'] = comments
        context['comment_form'] = CommentForm
        context['discount_percent'] = discount_percent
        return context
    
class BrandListView(generic.ListView):
    model = Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'

    def get_queryset(self):
        return Brand.objects.all()

    
