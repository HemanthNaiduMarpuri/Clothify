from django.urls import include, path
from .views import FavoriteView, FavoriteListView, CartView, cart_view, create_checkout_session, stripe_success, stripe_cancel, check_details_view, OrdersList, request_return

urlpatterns = [
    path('favorite/<int:pk>/', FavoriteView.as_view(), name='favorite'),
    path('favorite-list/', FavoriteListView.as_view(), name='favorite_list'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart'),
    path('cart-list/', cart_view, name='cart_list'),
    path('check-details/', check_details_view, name='check_details'),
    path('create-checkout-session/', create_checkout_session, name="create_checkout_session"),
    path('success/', stripe_success, name='success'),
    path('cancel/', stripe_cancel, name='cancel'),
    path('orders-list/', OrdersList.as_view(), name='orders_list'),
    path('return-request/<int:order_id>/', request_return, name='request_return'),
    path('coupon/', include('coupon.urls'))
]
