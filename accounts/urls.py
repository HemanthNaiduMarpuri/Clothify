from django.urls import path
from .views import ProfileView, CustomerProfileEditView

urlpatterns = [
    path('view/', ProfileView.as_view(), name='profile'),
    path('customer/edit-profile/', CustomerProfileEditView.as_view(), name='customer_profile_edit')
]
