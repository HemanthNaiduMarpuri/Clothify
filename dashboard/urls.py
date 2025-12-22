from django.urls import path
from .views import (DashboardView, AllProductsView, ProductDetailView, AllCategoriesView, AllBrandsView, AllCustomersView, AllDeliveryBoyView, ProductStockView, ApprovalView, AllOrdersView, update_order_status, PaidOrdersList, PendingOrdersList, OngoingOrdersList, CancelledOrdersList, DeliveredOrdersList, PaymentsView, create_product, UpdateProductView
                    , ProductDeleteView, BrandCreateView, BrandUpdateView, BrandDeleteView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, RequestReturnedOrdersList, UserOrdersView, update_complaint_status)

urlpatterns = [
    path('', DashboardView.as_view(), name='admin_dashboard'),
    path('products-list/', AllProductsView.as_view(), name='all_products'),
    path('admin-product-detail/<int:pk>/', ProductDetailView.as_view(), name='admin_product_detail'),
    path('category-list/', AllCategoriesView.as_view(), name='all_categories'),
    path('brands-list/', AllBrandsView.as_view(), name='all_brands'),
    path('all-customers/', AllCustomersView.as_view(), name='all_customers'),
    path('all-delivery-boys/', AllDeliveryBoyView.as_view(), name='all_deliveryboys'),
    path('product-inventory/', ProductStockView.as_view(), name='product_inventory'),
    path('approval-list/', ApprovalView.as_view(), name='approval_list'),
    path('all-orders/', AllOrdersView.as_view(), name='all_orders'),
    path('update-status/<int:id>/', update_order_status, name='update_status'),
    path('pending-orders/', PendingOrdersList.as_view(), name='pending_orders'),
    path('paid-orders/', PaidOrdersList.as_view(), name='paid_orders'),
    path('ongoing-orders/', OngoingOrdersList.as_view(), name='ongoing_orders'),
    path('delivered-orders/', DeliveredOrdersList.as_view(), name='delivered_orders'),
    path('request_returnrd_orders/', RequestReturnedOrdersList.as_view(), name='return_request_orders'),
    path('cancelled-orders/', CancelledOrdersList.as_view(), name='cancelled_orders'),
    path('payments-list/', PaymentsView.as_view(), name='payments'),
    path('create-product/', create_product, name='create_product'),
    path('update-product/<slug:slug>/', UpdateProductView.as_view(), name='update_product'),
    path('delete-product/<slug:slug>/', ProductDeleteView.as_view(), name='delete_product'),
    path('create-category/', CategoryCreateView.as_view(), name='create_category'),
    path('update-category/<slug:slug>/', CategoryUpdateView.as_view(), name='update_category'),
    path('delete-category/<slug:slug>/', CategoryDeleteView.as_view(), name='delete_category'),
    path('create-brand/', BrandCreateView.as_view(), name='create_brand'),
    path('update-brand/<slug:slug>/', BrandUpdateView.as_view(), name='update_brand'),
    path('delete-brand/<slug:slug>/', BrandDeleteView.as_view(), name='delete_brand'),
    path('user-orders/<int:user_id>/', UserOrdersView.as_view(), name='user_orders'),
    path('update-complaint/<int:pk>/status', update_complaint_status, name='update_complaint_status')
]
