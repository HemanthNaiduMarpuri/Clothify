from django.urls import include, path
from .views import ProductsListView, DiscountedProductsListView, ProductDetailView, BrandListView

urlpatterns = [
    path('list/', ProductsListView.as_view(), name='products_list'),
    path('discount-products/', DiscountedProductsListView.as_view(), name='discount_products_list'),
    path('product-detail/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('brand_list/', BrandListView.as_view(), name='brand_list'),
    path('orders/',include('orders.urls')),
    path('comment/', include('comments.urls'))
]
